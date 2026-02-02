from __future__ import annotations

import pytest

from linkedin_game_solver.games.zip.parser import parse_puzzle_dict, parse_puzzle_file


def test_parse_zip_puzzle_file() -> None:
    puzzle = parse_puzzle_file("data/curated/zip/zip_n4_01.json")
    assert puzzle.n == 4
    assert puzzle.numbers[1] == (0, 0)
    assert puzzle.numbers[2] == (1, 2)
    assert puzzle.numbers[3] == (3, 0)


def test_parse_zip_invalid_wall() -> None:
    payload = {
        "game": "zip",
        "n": 4,
        "numbers": [{"k": 1, "r": 0, "c": 0}],
        "walls": [{"r1": 0, "c1": 0, "r2": 2, "c2": 0}],
    }
    with pytest.raises(ValueError):
        parse_puzzle_dict(payload)
