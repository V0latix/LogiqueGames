"""Export puzzle datasets into a single JSON manifest."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from linkedin_game_solver.games.queens.parser import parse_puzzle_dict


@dataclass
class ExportStats:
    total_files: int = 0
    exported: int = 0
    skipped: int = 0


def _canonical_puzzle_payload(payload: dict) -> dict:
    return {
        "n": payload["n"],
        "regions": payload["regions"],
        "givens": payload.get("givens", {"queens": [], "blocked": []}),
    }


def _fingerprint(payload: dict) -> str:
    canonical = _canonical_puzzle_payload(payload)
    data = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _collect_json_files(input_dir: Path) -> list[Path]:
    if not input_dir.exists():
        msg = f"Input directory does not exist: {input_dir}"
        raise ValueError(msg)
    return sorted(p for p in input_dir.rglob("*.json") if p.is_file())


def export_dataset(
    input_dir: Path,
    output_path: Path,
    source: str,
    allow_duplicates: bool = False,
) -> ExportStats:
    files = _collect_json_files(input_dir)
    stats = ExportStats(total_files=len(files))

    puzzles: list[dict] = []
    seen: set[str] = set()

    next_id = 1
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            # Normalize regions to matrix when needed.
            if isinstance(payload.get("regions"), list) and payload.get("n") is not None:
                from .normalize import _normalize_puzzle  # local import to avoid cycles

                payload, _ = _normalize_puzzle(payload)
            parse_puzzle_dict(payload)
            fp = _fingerprint(payload)
            if fp in seen and not allow_duplicates:
                raise ValueError("duplicate puzzle detected")
            seen.add(fp)

            puzzles.append(
                {
                    "id": next_id,
                    "source": source,
                    "n": payload["n"],
                    "regions": payload["regions"],
                    "givens": payload.get("givens", {"queens": [], "blocked": []}),
                }
            )
            next_id += 1
            stats.exported += 1
        except Exception:  # noqa: BLE001
            stats.skipped += 1

    manifest = {
        "game": "queens",
        "version": 1,
        "puzzles": puzzles,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return stats


def load_manifest(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("game") != "queens" or "puzzles" not in payload:
        msg = f"Invalid manifest: {path}"
        raise ValueError(msg)
    return payload["puzzles"]


def fingerprints_from_manifest(puzzles: Iterable[dict]) -> list[str]:
    return [_fingerprint(puzzle) for puzzle in puzzles]
