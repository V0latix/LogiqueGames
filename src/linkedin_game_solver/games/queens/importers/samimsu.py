"""Importer for the MIT-licensed samimsu/queens-game-linkedin dataset."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from linkedin_game_solver.games.queens.parser import parse_puzzle_dict


@dataclass
class ImportStats:
    total_files: int = 0
    imported: int = 0
    skipped: int = 0


class ImportError(Exception):
    """Raised when importing should fail immediately."""


def _extract_bracket_block(text: str, key: str) -> str:
    key_index = text.find(key)
    if key_index == -1:
        msg = f"Key '{key}' not found"
        raise ValueError(msg)

    start = text.find("[", key_index)
    if start == -1:
        msg = f"No '[' found after '{key}'"
        raise ValueError(msg)

    depth = 0
    for idx in range(start, len(text)):
        char = text[idx]
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return text[start : idx + 1]

    msg = f"Unterminated bracket block for '{key}'"
    raise ValueError(msg)


def _strip_trailing_commas(value: str) -> str:
    # Remove trailing commas before a closing bracket.
    return re.sub(r",\s*\]", "]", value)


def _extract_size(text: str) -> int:
    match = re.search(r"\bsize\s*:\s*(\d+)", text)
    if not match:
        msg = "size not found"
        raise ValueError(msg)
    return int(match.group(1))


def _extract_color_regions(text: str) -> list[list[str]]:
    block = _extract_bracket_block(text, "colorRegions")
    block = _strip_trailing_commas(block)
    return json.loads(block)


def _convert_regions_to_int(grid: list[list[str]]) -> tuple[list[list[int]], dict[str, int]]:
    mapping: dict[str, int] = {}
    next_id = 0
    regions_int: list[list[int]] = []

    for row in grid:
        row_int: list[int] = []
        for cell in row:
            if cell not in mapping:
                mapping[cell] = next_id
                next_id += 1
            row_int.append(mapping[cell])
        regions_int.append(row_int)

    return regions_int, mapping


def _build_payload(n: int, regions: list[list[int]], level_id: str) -> dict:
    return {
        "game": "queens",
        "n": n,
        "regions": regions,
        "givens": {"queens": [], "blocked": []},
        "meta": {
            "source": "samimsu/queens-game-linkedin",
            "level_id": level_id,
        },
    }


def import_samimsu_dataset(
    source_root: Path,
    outdir: Path,
    on_invalid: str = "skip",
) -> ImportStats:
    if on_invalid not in {"skip", "fail"}:
        msg = "on_invalid must be 'skip' or 'fail'"
        raise ValueError(msg)

    levels_dir = source_root / "src" / "utils" / "community-levels"
    if not levels_dir.exists():
        msg = f"levels directory not found: {levels_dir}"
        raise ValueError(msg)

    outdir.mkdir(parents=True, exist_ok=True)

    stats = ImportStats()
    for path in sorted(levels_dir.glob("level*.ts")):
        stats.total_files += 1
        try:
            text = path.read_text(encoding="utf-8")
            size = _extract_size(text)
            color_regions = _extract_color_regions(text)

            if len(color_regions) != size or any(len(row) != size for row in color_regions):
                raise ValueError("colorRegions must be size x size")

            regions_int, mapping = _convert_regions_to_int(color_regions)
            if len(mapping) != size:
                raise ValueError("number of distinct regions must equal size")

            level_id = path.stem.replace("level", "") or path.stem
            payload = _build_payload(size, regions_int, level_id)

            # Validate using our parser to ensure compatibility.
            parse_puzzle_dict(payload)

            output_path = outdir / f"samimsu_level{level_id}.json"
            output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            stats.imported += 1
        except Exception as exc:  # noqa: BLE001 - aggregated import errors are expected here.
            stats.skipped += 1
            if on_invalid == "fail":
                raise ImportError(f"Failed to import {path.name}: {exc}") from exc
            print(f"[import-samimsu] Skipped {path.name}: {exc}")

    return stats
