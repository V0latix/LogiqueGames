#!/usr/bin/env python3
"""Extract LinkedIn Queens/Zip puzzles from selected frames using GPT vision.

This script is designed to replace the fragile CV-based steps (04 + 06) by sending
the chosen screenshot (chosen_frame.png) directly to an OpenAI vision-capable model.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, cast

from pipeline_utils import dump_json, ensure_dir, load_json, relative_to_cwd, utc_now_iso


Game = Literal["queens", "zip", "auto"]


SYSTEM_PROMPT = (
    "You are an expert puzzle extractor for LinkedIn games. You receive a screenshot of a "
    "LinkedIn puzzle (either Queens or Zip) and must return a valid JSON object describing "
    "the puzzle. Return ONLY valid JSON, no explanation, no markdown code block, just raw JSON."
)

QUEENS_USER_PROMPT = """This is a Queens puzzle screenshot from LinkedIn.

The grid is n×n. Each cell belongs to exactly one colored region. There are n distinct colors/regions.

Return a JSON object with this exact schema:
{
  "game": "queens",
  "n": <integer, grid size>,
  "regions": [
    [<region_id for row 0>, ...],
    [<region_id for row 1>, ...],
    ...
  ]
}

Rules:
- regions is an n×n matrix of integers (0-indexed)
- Region IDs are assigned in reading order: the first color encountered (top-left to bottom-right) gets ID 0, the next new color gets ID 1, etc.
- Every cell in the same colored area must have the same region ID
- Each region ID must appear at least once
- IDs must be consecutive integers from 0 to n-1

Return ONLY the JSON object, no markdown, no explanation."""

ZIP_USER_PROMPT = """This is a Zip puzzle screenshot from LinkedIn.

The grid is n×n. It contains:
1. Numbered circles (checkpoints): black circles with a white number inside, from 1 to some maximum K
2. Thick walls: bold/thick borders between some adjacent cells (NOT the outer border)

Return a JSON object with this exact schema:
{
  "game": "zip",
  "n": <integer, grid size>,
  "numbers": [
    {"k": <number>, "r": <row 0-indexed>, "c": <col 0-indexed>},
    ...
  ],
  "walls": [
    {"r1": <row>, "c1": <col>, "r2": <row>, "c2": <col>},
    ...
  ]
}

Rules:
- numbers: list all numbered circles, sorted by k ascending
- walls: each wall entry has (r1,c1) and (r2,c2) being the two adjacent cells on either side of a thick interior wall. Adjacent means same row with consecutive columns, or same column with consecutive rows. Do NOT include the outer border of the grid.
- rows and columns are 0-indexed (top-left is r=0, c=0)

Return ONLY the JSON object, no markdown, no explanation."""

AUTO_USER_PROMPT = """This is a LinkedIn puzzle screenshot. First identify if it's a Queens puzzle (colored regions, no numbers in cells) or a Zip puzzle (numbered circles and thick walls).

Then extract the puzzle and return a JSON object.

For Queens, return:
{"game": "queens", "n": <int>, "regions": [[...], ...]}

For Zip, return:
{"game": "zip", "n": <int>, "numbers": [{"k":..,"r":..,"c":..},...], "walls": [{"r1":..,"c1":..,"r2":..,"c2":..},...]}

Return ONLY the JSON object."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract Queens/Zip puzzles via GPT vision")
    parser.add_argument(
        "--selection-metadata",
        default="zip_archive/metadata/selected_frames.json",
        help="Path to selected_frames.json",
    )
    parser.add_argument(
        "--index",
        default="zip_archive/metadata/index.json",
        help="Path to index.json (fallback when selection metadata lacks a chosen_frame)",
    )
    parser.add_argument(
        "--out-dir",
        default="zip_archive/puzzles_gpt",
        help="Output directory for puzzle JSON files",
    )
    parser.add_argument(
        "--manifest",
        default="zip_archive/metadata/puzzles_gpt_manifest.json",
        help="Output manifest path",
    )
    parser.add_argument(
        "--game",
        choices=["queens", "zip", "auto"],
        default="auto",
        help='Force game type: "queens", "zip", or "auto"',
    )
    parser.add_argument("--model", default="gpt-4.1", help="OpenAI model to use")
    parser.add_argument("--limit", type=int, default=None, help="Process only the first N entries")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output files")
    parser.add_argument("--verbose", action="store_true", help="Print per-entry status")
    parser.add_argument("--only-video", default=None, help="Process only a specific video_basename")
    parser.add_argument(
        "--api-key",
        default=None,
        help="OpenAI API key (default: reads OPENAI_API_KEY env var)",
    )
    return parser.parse_args()


def _resolve_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def output_filename(entry: dict, fallback_idx: int) -> str:
    puzzle_number = entry.get("puzzle_number")
    num_part = f"#{puzzle_number:03d}" if isinstance(puzzle_number, int) else "#unknown"
    date_part = str(entry.get("puzzle_date") or "date_unknown")
    basename = str(entry.get("video_basename") or f"video_{fallback_idx:03d}")
    return f"{num_part}_{date_part}__{basename}.json"


def _puzzle_name(game: str, entry: dict) -> str | None:
    if game != "queens":
        return None
    puzzle_number = entry.get("puzzle_number")
    puzzle_date = entry.get("puzzle_date")
    if isinstance(puzzle_number, int) and isinstance(puzzle_date, str) and puzzle_date:
        return f"Queens #{puzzle_number} - {puzzle_date}"
    if isinstance(puzzle_number, int):
        return f"Queens #{puzzle_number}"
    return None


_FENCE_RE = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```", re.IGNORECASE)


def parse_gpt_response(raw: str) -> dict[str, Any]:
    """Parse model content into a JSON object.

    Handles the common failure mode where the model wraps JSON into markdown fences.
    """
    text = (raw or "").strip()
    if not text:
        raise ValueError("empty response")

    fence_match = _FENCE_RE.search(text)
    if fence_match:
        text = fence_match.group(1).strip()

    # If the response contains extra text, attempt to extract the outermost JSON object.
    if not text.startswith("{"):
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start : end + 1].strip()

    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("response JSON is not an object")
    return cast(dict[str, Any], payload)


def _require_int(value: Any, field: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be int")
    if not isinstance(value, int):
        raise ValueError(f"{field} must be int")
    return int(value)


def validate_queens(payload: dict[str, Any]) -> None:
    if payload.get("game") != "queens":
        raise ValueError("game must be queens")
    n = _require_int(payload.get("n"), "n")
    if not (4 <= n <= 15):
        raise ValueError("n out of range")

    regions = payload.get("regions")
    if not isinstance(regions, list) or len(regions) != n:
        raise ValueError("regions must be an n×n matrix")

    flat: list[int] = []
    for r, row in enumerate(regions):
        if not isinstance(row, list) or len(row) != n:
            raise ValueError(f"regions row {r} has wrong length")
        for c, value in enumerate(row):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"regions[{r}][{c}] must be int")
            flat.append(int(value))

    ids = sorted(set(flat))
    expected = list(range(n))
    if ids != expected:
        raise ValueError(f"region ids must be consecutive 0..{n-1} (got {ids})")


def validate_zip(payload: dict[str, Any]) -> None:
    if payload.get("game") != "zip":
        raise ValueError("game must be zip")
    n = _require_int(payload.get("n"), "n")
    if not (3 <= n <= 15):
        raise ValueError("n out of range")

    numbers = payload.get("numbers")
    if not isinstance(numbers, list) or len(numbers) < 2:
        raise ValueError("numbers must be a non-empty list (>=2)")

    seen_k: set[int] = set()
    for idx, item in enumerate(numbers):
        if not isinstance(item, dict):
            raise ValueError(f"numbers[{idx}] must be an object")
        k = _require_int(item.get("k"), f"numbers[{idx}].k")
        r = _require_int(item.get("r"), f"numbers[{idx}].r")
        c = _require_int(item.get("c"), f"numbers[{idx}].c")
        if k in seen_k:
            raise ValueError("numbers.k must be unique")
        seen_k.add(k)
        if not (0 <= r < n and 0 <= c < n):
            raise ValueError("numbers coordinates out of range")

    walls = payload.get("walls")
    if walls is None:
        return
    if not isinstance(walls, list):
        raise ValueError("walls must be a list")
    for idx, wall in enumerate(walls):
        if not isinstance(wall, dict):
            raise ValueError(f"walls[{idx}] must be an object")
        r1 = _require_int(wall.get("r1"), f"walls[{idx}].r1")
        c1 = _require_int(wall.get("c1"), f"walls[{idx}].c1")
        r2 = _require_int(wall.get("r2"), f"walls[{idx}].r2")
        c2 = _require_int(wall.get("c2"), f"walls[{idx}].c2")
        if not (0 <= r1 < n and 0 <= c1 < n and 0 <= r2 < n and 0 <= c2 < n):
            raise ValueError("walls coordinates out of range")
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            raise ValueError("walls endpoints must be adjacent cells")


def _prompt_for_game(game: Game) -> str:
    if game == "queens":
        return QUEENS_USER_PROMPT
    if game == "zip":
        return ZIP_USER_PROMPT
    return AUTO_USER_PROMPT


def _read_api_key(cli_value: str | None) -> str | None:
    if cli_value:
        return cli_value.strip() or None
    value = os.environ.get("OPENAI_API_KEY")
    return value.strip() if value else None


def call_openai_vision(
    *,
    api_key: str,
    model: str,
    user_prompt: str,
    image_path: Path,
    max_retries: int = 3,
) -> str:
    """Call OpenAI Chat Completions with an inlined PNG as data URL."""
    try:
        from openai import OpenAI  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "Missing dependency: openai. Install it with `pip install openai`."
        ) from exc

    with image_path.open("rb") as handle:
        image_data = base64.b64encode(handle.read()).decode("utf-8")

    client = OpenAI(api_key=api_key)

    # Basic exponential backoff on transient errors (rate-limit/network).
    delays = [5, 15, 30]
    last_error: Exception | None = None
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_data}",
                                    "detail": "high",
                                },
                            },
                            {"type": "text", "text": user_prompt},
                        ],
                    },
                ],
                max_tokens=4096,
                temperature=0,
            )
            content = response.choices[0].message.content
            if content is None:
                raise RuntimeError("OpenAI response had empty message content")
            return str(content).strip()
        except Exception as exc:  # pragma: no cover
            last_error = exc
            if attempt >= max_retries - 1:
                break
            time.sleep(delays[min(attempt, len(delays) - 1)])

    assert last_error is not None  # for type checkers
    raise last_error


@dataclass(frozen=True)
class SourceEntry:
    video_basename: str
    meta: dict[str, Any]
    image_path: Path | None


def _build_source_entries(
    selection_payload: dict[str, Any],
    index_payload: dict[str, Any],
    *,
    only_video: str | None,
) -> list[SourceEntry]:
    index_by_basename: dict[str, dict[str, Any]] = {}
    for entry in index_payload.get("entries", []) if isinstance(index_payload.get("entries"), list) else []:
        if isinstance(entry, dict) and entry.get("video_basename"):
            index_by_basename[str(entry["video_basename"])] = entry

    results: list[SourceEntry] = []

    videos = selection_payload.get("videos")
    if isinstance(videos, list) and videos:
        for entry in videos:
            if not isinstance(entry, dict):
                continue
            basename = entry.get("video_basename")
            if not basename:
                continue
            if only_video and str(basename) != only_video:
                continue
            if entry.get("status") != "ok":
                continue
            chosen = entry.get("chosen_frame")
            image = _resolve_path(str(chosen)) if chosen else None

            index_entry = index_by_basename.get(str(basename), {})

            # Merge metadata, preferring index.json for puzzle_number/date (derived).
            merged_meta: dict[str, Any] = {
                "video_basename": str(basename),
                "playlist_index": index_entry.get("playlist_index", entry.get("playlist_index")),
                "video_id": index_entry.get("video_id", entry.get("video_id")),
                "puzzle_number": index_entry.get("puzzle_number"),
                "puzzle_date": index_entry.get("puzzle_date"),
                "source_url": index_entry.get("source_url", entry.get("source_url")),
                "frame_timestamp": index_entry.get("frame_timestamp", entry.get("frame_timestamp")),
            }

            if image is None:
                # selection metadata missing: try index paths.
                paths = index_entry.get("paths") if isinstance(index_entry.get("paths"), dict) else {}
                fallback = None
                if isinstance(paths, dict):
                    fallback = paths.get("chosen_frame") or paths.get("grid_image")
                image = _resolve_path(str(fallback)) if fallback else None

            results.append(SourceEntry(video_basename=str(basename), meta=merged_meta, image_path=image))

        return results

    # No selection metadata (or empty): fallback to index entries.
    for basename, index_entry in index_by_basename.items():
        if only_video and basename != only_video:
            continue
        if not isinstance(index_entry, dict):
            continue
        paths = index_entry.get("paths") if isinstance(index_entry.get("paths"), dict) else {}
        fallback = None
        if isinstance(paths, dict):
            fallback = paths.get("chosen_frame") or paths.get("grid_image")
        image = _resolve_path(str(fallback)) if fallback else None
        merged_meta = {
            "video_basename": basename,
            "playlist_index": index_entry.get("playlist_index"),
            "video_id": index_entry.get("video_id"),
            "puzzle_number": index_entry.get("puzzle_number"),
            "puzzle_date": index_entry.get("puzzle_date"),
            "source_url": index_entry.get("source_url"),
            "frame_timestamp": index_entry.get("frame_timestamp"),
        }
        results.append(SourceEntry(video_basename=basename, meta=merged_meta, image_path=image))

    return results


def _enrich_and_normalize_payload(
    extracted: dict[str, Any],
    *,
    entry_meta: dict[str, Any],
    image_path: Path,
    conversion: str,
) -> dict[str, Any]:
    game = extracted.get("game")
    if game == "queens":
        validate_queens(extracted)
        name = _puzzle_name("queens", entry_meta)
        payload = {
            "game": "queens",
            "n": int(extracted["n"]),
            "regions": extracted["regions"],
            "givens": {"queens": [], "blocked": []},
            "meta": {
                "video_id": entry_meta.get("video_id"),
                "playlist_index": entry_meta.get("playlist_index"),
                "puzzle_number": entry_meta.get("puzzle_number"),
                "puzzle_date": entry_meta.get("puzzle_date"),
                "source_url": entry_meta.get("source_url"),
                "frame_timestamp": entry_meta.get("frame_timestamp"),
                "grid_image": relative_to_cwd(image_path),
                "name": name,
                "conversion": conversion,
            },
        }
        return payload

    if game == "zip":
        validate_zip(extracted)
        numbers = extracted.get("numbers") if isinstance(extracted.get("numbers"), list) else []
        numbers = sorted(
            [
                {"k": int(x["k"]), "r": int(x["r"]), "c": int(x["c"])}
                for x in numbers
                if isinstance(x, dict) and "k" in x and "r" in x and "c" in x
            ],
            key=lambda item: item["k"],
        )
        walls = extracted.get("walls") if isinstance(extracted.get("walls"), list) else []
        walls_norm = []
        for w in walls:
            if not isinstance(w, dict):
                continue
            if not all(k in w for k in ("r1", "c1", "r2", "c2")):
                continue
            walls_norm.append(
                {
                    "r1": int(w["r1"]),
                    "c1": int(w["c1"]),
                    "r2": int(w["r2"]),
                    "c2": int(w["c2"]),
                }
            )
        walls_norm = sorted(walls_norm, key=lambda w: (w["r1"], w["c1"], w["r2"], w["c2"]))
        payload = {
            "game": "zip",
            "n": int(extracted["n"]),
            "numbers": numbers,
            "walls": walls_norm,
            "meta": {
                "video_id": entry_meta.get("video_id"),
                "playlist_index": entry_meta.get("playlist_index"),
                "puzzle_number": entry_meta.get("puzzle_number"),
                "puzzle_date": entry_meta.get("puzzle_date"),
                "source_url": entry_meta.get("source_url"),
                "frame_timestamp": entry_meta.get("frame_timestamp"),
                "grid_image": relative_to_cwd(image_path),
                "conversion": conversion,
            },
        }
        return payload

    raise ValueError(f"unknown game: {game!r}")


def convert_one(
    source: SourceEntry,
    *,
    out_dir: Path,
    api_key: str | None,
    model: str,
    forced_game: Game,
    force: bool,
) -> dict[str, Any]:
    image_path = source.image_path
    if image_path is None:
        return {
            "video_basename": source.video_basename,
            "playlist_index": source.meta.get("playlist_index"),
            "video_id": source.meta.get("video_id"),
            "puzzle_number": source.meta.get("puzzle_number"),
            "puzzle_date": source.meta.get("puzzle_date"),
            "grid_image": None,
            "status": "needs_review",
            "error": "missing chosen_frame/grid_image path",
        }

    if not image_path.exists():
        return {
            "video_basename": source.video_basename,
            "playlist_index": source.meta.get("playlist_index"),
            "video_id": source.meta.get("video_id"),
            "puzzle_number": source.meta.get("puzzle_number"),
            "puzzle_date": source.meta.get("puzzle_date"),
            "grid_image": relative_to_cwd(image_path),
            "status": "needs_review",
            "error": f"image not found: {relative_to_cwd(image_path)}",
        }

    file_name = output_filename(source.meta, fallback_idx=int(source.meta.get("playlist_index") or 0))
    out_path = out_dir / file_name

    if out_path.exists() and not force:
        return {
            "video_basename": source.video_basename,
            "playlist_index": source.meta.get("playlist_index"),
            "video_id": source.meta.get("video_id"),
            "puzzle_number": source.meta.get("puzzle_number"),
            "puzzle_date": source.meta.get("puzzle_date"),
            "grid_image": relative_to_cwd(image_path),
            "json_path": relative_to_cwd(out_path),
            "status": "ok",
            "skipped": True,
        }

    if not api_key:
        return {
            "video_basename": source.video_basename,
            "playlist_index": source.meta.get("playlist_index"),
            "video_id": source.meta.get("video_id"),
            "puzzle_number": source.meta.get("puzzle_number"),
            "puzzle_date": source.meta.get("puzzle_date"),
            "grid_image": relative_to_cwd(image_path),
            "status": "needs_review",
            "error": "missing OPENAI_API_KEY (or --api-key)",
        }

    user_prompt = _prompt_for_game(forced_game)

    try:
        raw = call_openai_vision(
            api_key=api_key,
            model=model,
            user_prompt=user_prompt,
            image_path=image_path,
        )
    except Exception as exc:  # pragma: no cover
        return {
            "video_basename": source.video_basename,
            "playlist_index": source.meta.get("playlist_index"),
            "video_id": source.meta.get("video_id"),
            "puzzle_number": source.meta.get("puzzle_number"),
            "puzzle_date": source.meta.get("puzzle_date"),
            "grid_image": relative_to_cwd(image_path),
            "status": "needs_review",
            "error": f"api error: {exc}",
        }

    try:
        extracted = parse_gpt_response(raw)
    except Exception as exc:
        return {
            "video_basename": source.video_basename,
            "playlist_index": source.meta.get("playlist_index"),
            "video_id": source.meta.get("video_id"),
            "puzzle_number": source.meta.get("puzzle_number"),
            "puzzle_date": source.meta.get("puzzle_date"),
            "grid_image": relative_to_cwd(image_path),
            "status": "needs_review",
            "error": f"invalid json: {exc}",
        }

    if forced_game in ("queens", "zip") and extracted.get("game") != forced_game:
        return {
            "video_basename": source.video_basename,
            "playlist_index": source.meta.get("playlist_index"),
            "video_id": source.meta.get("video_id"),
            "puzzle_number": source.meta.get("puzzle_number"),
            "puzzle_date": source.meta.get("puzzle_date"),
            "grid_image": relative_to_cwd(image_path),
            "status": "needs_review",
            "error": f"validation: game mismatch (expected {forced_game}, got {extracted.get('game')})",
        }

    try:
        payload = _enrich_and_normalize_payload(
            extracted,
            entry_meta=source.meta,
            image_path=image_path,
            conversion="gpt_vision_v1",
        )
    except Exception as exc:
        return {
            "video_basename": source.video_basename,
            "playlist_index": source.meta.get("playlist_index"),
            "video_id": source.meta.get("video_id"),
            "puzzle_number": source.meta.get("puzzle_number"),
            "puzzle_date": source.meta.get("puzzle_date"),
            "grid_image": relative_to_cwd(image_path),
            "status": "needs_review",
            "error": f"validation: {exc}",
        }

    ensure_dir(out_path.parent)
    dump_json(out_path, payload)

    return {
        "video_basename": source.video_basename,
        "playlist_index": source.meta.get("playlist_index"),
        "video_id": source.meta.get("video_id"),
        "puzzle_number": source.meta.get("puzzle_number"),
        "puzzle_date": source.meta.get("puzzle_date"),
        "grid_image": relative_to_cwd(image_path),
        "json_path": relative_to_cwd(out_path),
        "n": payload.get("n"),
        "status": "ok",
        "error": None,
    }


def main() -> int:
    args = parse_args()

    selection_path = Path(args.selection_metadata)
    index_path = Path(args.index)
    out_dir = Path(args.out_dir)
    manifest_path = Path(args.manifest)
    forced_game = cast(Game, args.game)

    ensure_dir(out_dir)
    ensure_dir(manifest_path.parent)

    selection_payload = load_json(selection_path, default={})
    index_payload = load_json(index_path, default={})

    sources = _build_source_entries(
        selection_payload,
        index_payload,
        only_video=args.only_video,
    )

    if args.limit is not None:
        sources = sources[: args.limit]

    if not sources:
        print("No entries to process (selection metadata empty and index empty).")
        return 0

    api_key = _read_api_key(args.api_key)

    results: list[dict[str, Any]] = []
    for idx, source in enumerate(sources, start=1):
        result = convert_one(
            source,
            out_dir=out_dir,
            api_key=api_key,
            model=str(args.model),
            forced_game=forced_game,
            force=bool(args.force),
        )
        results.append(result)

        if args.verbose:
            status = result.get("status")
            name = source.video_basename
            print(f"[{idx}/{len(sources)}] {name} -> {status}")

    ok_count = sum(1 for item in results if item.get("status") == "ok")
    review_count = len(results) - ok_count

    payload = {
        "generated_at": utc_now_iso(),
        "model": str(args.model),
        "game": str(args.game),
        "selection_metadata": relative_to_cwd(selection_path),
        "source_index": relative_to_cwd(index_path),
        "count": len(results),
        "ok": ok_count,
        "needs_review": review_count,
        "entries": sorted(
            results,
            key=lambda item: (
                item.get("playlist_index") is None,
                item.get("playlist_index") or 10**9,
                item.get("video_basename", ""),
            ),
        ),
    }

    dump_json(manifest_path, payload)
    print(f"Wrote puzzles manifest: {manifest_path} (ok={ok_count}, needs_review={review_count})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
