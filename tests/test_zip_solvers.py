from __future__ import annotations

from linkedin_game_solver.games.zip.model import ZipSolution
from linkedin_game_solver.games.zip.parser import parse_puzzle_dict, parse_puzzle_file
from linkedin_game_solver.games.zip.solver_baseline import solve_baseline
from linkedin_game_solver.games.zip.solver_heuristic import solve_heuristic, solve_heuristic_nolcv
from linkedin_game_solver.games.zip.validator import validate_solution


def test_zip_baseline_solves_simple() -> None:
    payload = {
        "game": "zip",
        "n": 2,
        "numbers": [{"k": 1, "r": 0, "c": 0}],
        "walls": [],
    }
    puzzle = parse_puzzle_dict(payload)
    result = solve_baseline(puzzle)
    assert result.solved, result.error
    assert result.solution is not None
    validation = validate_solution(puzzle, result.solution)
    assert validation.ok, validation.reason


def test_zip_baseline_handles_curated() -> None:
    puzzle = parse_puzzle_file("data/curated/zip/zip_n4_01.json")
    result = solve_baseline(puzzle, time_limit_s=1.0)
    assert result.solved, result.error
    assert result.solution is not None
    validation = validate_solution(puzzle, result.solution)
    assert validation.ok, validation.reason


def test_zip_heuristic_handles_curated() -> None:
    puzzle = parse_puzzle_file("data/curated/zip/zip_n4_01.json")
    result = solve_heuristic(puzzle, time_limit_s=1.0)
    assert result.solved, result.error
    assert result.solution is not None
    validation = validate_solution(puzzle, result.solution)
    assert validation.ok, validation.reason


def test_zip_heuristic_nolcv_handles_curated() -> None:
    puzzle = parse_puzzle_file("data/curated/zip/zip_n4_01.json")
    result = solve_heuristic_nolcv(puzzle, time_limit_s=1.0)
    assert result.solved, result.error
    assert result.solution is not None
    validation = validate_solution(puzzle, result.solution)
    assert validation.ok, validation.reason


def test_zip_baseline_rejects_bad_solution() -> None:
    payload = {
        "game": "zip",
        "n": 2,
        "numbers": [{"k": 1, "r": 0, "c": 0}],
        "walls": [],
    }
    puzzle = parse_puzzle_dict(payload)
    bad = ZipSolution(path=[(0, 0), (0, 1), (0, 1), (1, 1)])
    result = validate_solution(puzzle, bad)
    assert not result.ok
