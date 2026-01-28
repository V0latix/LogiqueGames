from __future__ import annotations

import json
from pathlib import Path

from linkedin_game_solver.datasets.exporter import (
    export_dataset,
    fingerprints_from_manifest,
    load_manifest,
)
from linkedin_game_solver.games.queens.generator import generate_puzzle_payload


def _write_puzzle(path: Path, n: int, seed: int) -> None:
    payload, _solution = generate_puzzle_payload(n=n, seed=seed)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_export_dataset_uniqueness(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    _write_puzzle(input_dir / "a.json", n=6, seed=1)
    _write_puzzle(input_dir / "b.json", n=6, seed=2)

    out = tmp_path / "puzzles.json"
    stats = export_dataset(input_dir, out, source="imported")
    assert stats.exported == 2

    puzzles = load_manifest(out)
    hashes = fingerprints_from_manifest(puzzles)
    assert len(set(hashes)) == len(hashes)


def test_export_dataset_skips_duplicates(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    _write_puzzle(input_dir / "a.json", n=6, seed=1)
    # Duplicate: same payload
    _write_puzzle(input_dir / "b.json", n=6, seed=1)

    out = tmp_path / "puzzles.json"
    stats = export_dataset(input_dir, out, source="imported")
    assert stats.exported == 1
    assert stats.skipped == 1

    puzzles = load_manifest(out)
    assert len(puzzles) == 1


def test_export_dataset_allows_duplicates(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    _write_puzzle(input_dir / "a.json", n=6, seed=1)
    _write_puzzle(input_dir / "b.json", n=6, seed=1)

    out = tmp_path / "puzzles.json"
    stats = export_dataset(input_dir, out, source="imported", allow_duplicates=True)
    assert stats.exported == 2

    puzzles = load_manifest(out)
    assert len(puzzles) == 2
