"""Normalize puzzle datasets to ensure matrix regions format."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class NormalizeStats:
    total: int = 0
    converted: int = 0
    unchanged: int = 0
    skipped: int = 0


def _is_matrix(regions: Any, n: int) -> bool:
    if not isinstance(regions, list) or len(regions) != n:
        return False
    return all(isinstance(row, list) and len(row) == n for row in regions)


def _to_matrix(regions: list[int], n: int) -> list[list[int]]:
    if len(regions) != n * n:
        msg = f"Flat regions length {len(regions)} does not match n*n={n*n}"
        raise ValueError(msg)
    return [regions[i * n : (i + 1) * n] for i in range(n)]


def _normalize_puzzle(puzzle: dict) -> tuple[dict, bool]:
    n = int(puzzle["n"])
    regions = puzzle["regions"]
    if _is_matrix(regions, n):
        return puzzle, False
    if isinstance(regions, list) and all(isinstance(x, int) for x in regions):
        puzzle["regions"] = _to_matrix(regions, n)
        return puzzle, True
    msg = "regions is not a valid matrix or flat list"
    raise ValueError(msg)


def _normalize_manifest(payload: dict) -> NormalizeStats:
    stats = NormalizeStats()
    puzzles = payload.get("puzzles", [])
    for puzzle in puzzles:
        stats.total += 1
        try:
            _, changed = _normalize_puzzle(puzzle)
            if changed:
                stats.converted += 1
            else:
                stats.unchanged += 1
        except Exception:
            stats.skipped += 1
    return stats


def normalize_dataset(input_path: Path, output_path: Path | None = None) -> NormalizeStats:
    if output_path is None:
        output_path = input_path

    if input_path.is_dir():
        stats = NormalizeStats()
        files = sorted(p for p in input_path.rglob("*.json") if p.is_file())
        for path in files:
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                if payload.get("game") == "queens" and "regions" in payload:
                    stats.total += 1
                    _, changed = _normalize_puzzle(payload)
                    if changed:
                        stats.converted += 1
                    else:
                        stats.unchanged += 1
                    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            except Exception:
                stats.skipped += 1
        return stats

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if payload.get("game") == "queens" and "puzzles" in payload:
        stats = _normalize_manifest(payload)
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return stats

    # Single puzzle JSON
    stats = NormalizeStats(total=1)
    try:
        _, changed = _normalize_puzzle(payload)
        if changed:
            stats.converted += 1
        else:
            stats.unchanged += 1
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    except Exception:
        stats.skipped += 1
    return stats
