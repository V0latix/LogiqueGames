from __future__ import annotations

from linkedin_game_solver.games.zip.parser import parse_puzzle_dict
from linkedin_game_solver.games.zip.solver_counting import count_solutions


def test_zip_counting_finds_multiple() -> None:
    payload = {
        "game": "zip",
        "n": 2,
        "numbers": [{"k": 1, "r": 0, "c": 0}],
        "walls": [],
    }
    puzzle = parse_puzzle_dict(payload)
    result = count_solutions(puzzle, time_limit_s=0.5, max_solutions=2)
    assert not result.timed_out
    assert result.solutions == 2


def test_zip_counting_unique_with_full_checkpoints() -> None:
    payload = {
        "game": "zip",
        "n": 2,
        "numbers": [
            {"k": 1, "r": 0, "c": 0},
            {"k": 2, "r": 0, "c": 1},
            {"k": 3, "r": 1, "c": 1},
            {"k": 4, "r": 1, "c": 0},
        ],
        "walls": [],
    }
    puzzle = parse_puzzle_dict(payload)
    result = count_solutions(puzzle, time_limit_s=0.5, max_solutions=2)
    assert not result.timed_out
    assert result.solutions == 1
