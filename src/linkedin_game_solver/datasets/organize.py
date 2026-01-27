"""Utilities to organize puzzle datasets by size."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass
class OrganizeStats:
    total_files: int = 0
    moved: int = 0
    skipped: int = 0


def _read_size(path: Path) -> int:
    payload = json.loads(path.read_text(encoding="utf-8"))
    size = int(payload.get("n"))
    if size <= 0:
        msg = f"Invalid size in {path.name}"
        raise ValueError(msg)
    return size


def _unique_destination(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem = dest.stem
    suffix = dest.suffix
    parent = dest.parent
    for idx in range(1, 10_000):
        candidate = parent / f"{stem}_dup{idx}{suffix}"
        if not candidate.exists():
            return candidate
    msg = f"Unable to find unique filename for {dest.name}"
    raise ValueError(msg)


def organize_by_size(
    input_dir: Path,
    output_dir: Path,
    mode: str = "move",
) -> OrganizeStats:
    if mode not in {"move", "copy"}:
        msg = "mode must be 'move' or 'copy'"
        raise ValueError(msg)

    if not input_dir.exists():
        msg = f"Input directory does not exist: {input_dir}"
        raise ValueError(msg)

    output_dir.mkdir(parents=True, exist_ok=True)

    stats = OrganizeStats()
    for path in sorted(p for p in input_dir.glob("*.json") if p.is_file()):
        stats.total_files += 1
        try:
            size = _read_size(path)
            size_dir = output_dir / f"size_{size}"
            size_dir.mkdir(parents=True, exist_ok=True)

            destination = _unique_destination(size_dir / path.name)
            if mode == "move":
                shutil.move(str(path), str(destination))
            else:
                shutil.copy2(str(path), str(destination))
            stats.moved += 1
        except Exception:  # noqa: BLE001 - allow per-file skip
            stats.skipped += 1

    return stats
