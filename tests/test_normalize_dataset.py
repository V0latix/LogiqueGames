from __future__ import annotations

import json
from pathlib import Path

from linkedin_game_solver.datasets.normalize import normalize_dataset


def test_normalize_flat_regions_to_matrix(tmp_path: Path) -> None:
    payload = {
        "game": "queens",
        "n": 3,
        "regions": [0, 1, 2, 0, 1, 2, 0, 1, 2],
        "givens": {"queens": [], "blocked": []},
    }
    path = tmp_path / "puzzle.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    stats = normalize_dataset(path)
    assert stats.converted == 1

    normalized = json.loads(path.read_text(encoding="utf-8"))
    assert normalized["regions"] == [[0, 1, 2], [0, 1, 2], [0, 1, 2]]


def test_normalize_manifest(tmp_path: Path) -> None:
    payload = {
        "game": "queens",
        "version": 1,
        "puzzles": [
            {
                "id": 1,
                "source": "imported",
                "n": 2,
                "regions": [0, 1, 0, 1],
                "givens": {"queens": [], "blocked": []},
            }
        ],
    }
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    stats = normalize_dataset(path)
    assert stats.converted == 1

    normalized = json.loads(path.read_text(encoding="utf-8"))
    assert normalized["puzzles"][0]["regions"] == [[0, 1], [0, 1]]
