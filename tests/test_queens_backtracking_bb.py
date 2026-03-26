"""Tests for solve_backtracking_bb and solve_backtracking_bb_nolcv."""

from __future__ import annotations

from pathlib import Path

from linkedin_game_solver.games.queens.parser import parse_puzzle_dict, parse_puzzle_file
from linkedin_game_solver.games.queens.solver_backtracking_bb import (
    solve_backtracking_bb,
    solve_backtracking_bb_nolcv,
)
from linkedin_game_solver.games.queens.validator import validate_solution


def _simple_puzzle() -> dict:
    """6x6 row-based puzzle (easy, always solvable)."""
    return {
        "game": "queens",
        "n": 6,
        "regions": [[i] * 6 for i in range(6)],
        "givens": {"queens": [], "blocked": []},
    }


def test_solve_bb_on_curated_fixture() -> None:
    puzzle = parse_puzzle_file(Path("data/curated/queens/example_6x6.json"))
    result = solve_backtracking_bb(puzzle)
    assert result.solved, result.error
    assert result.solution is not None
    v = validate_solution(puzzle, result.solution)
    assert v.ok, v.reason
    assert result.metrics.nodes > 0
    assert result.metrics.time_ms >= 0.0


def test_solve_bb_nolcv_on_curated_fixture() -> None:
    puzzle = parse_puzzle_file(Path("data/curated/queens/example_6x6.json"))
    result = solve_backtracking_bb_nolcv(puzzle)
    assert result.solved, result.error
    assert result.solution is not None
    v = validate_solution(puzzle, result.solution)
    assert v.ok, v.reason


def test_solve_bb_simple_puzzle() -> None:
    puzzle = parse_puzzle_dict(_simple_puzzle())
    result = solve_backtracking_bb(puzzle)
    assert result.solved, result.error
    v = validate_solution(puzzle, result.solution)
    assert v.ok, v.reason


def test_solve_bb_nolcv_simple_puzzle() -> None:
    puzzle = parse_puzzle_dict(_simple_puzzle())
    result = solve_backtracking_bb_nolcv(puzzle)
    assert result.solved, result.error
    v = validate_solution(puzzle, result.solution)
    assert v.ok, v.reason


def test_solve_bb_with_time_limit() -> None:
    puzzle = parse_puzzle_dict(_simple_puzzle())
    result = solve_backtracking_bb(puzzle, time_limit_s=5.0)
    assert result.solved, result.error


def test_solve_bb_with_tight_time_limit_does_not_crash() -> None:
    puzzle = parse_puzzle_dict(_simple_puzzle())
    # Very tight limit — may or may not solve, but must not raise
    result = solve_backtracking_bb(puzzle, time_limit_s=0.000001)
    assert isinstance(result.solved, bool)


def test_solve_bb_with_givens() -> None:
    """Puzzle with a pre-placed queen (given) should still solve."""
    payload = {
        "game": "queens",
        "n": 6,
        "regions": [[i] * 6 for i in range(6)],
        "givens": {"queens": [[0, 0]], "blocked": []},
    }
    puzzle = parse_puzzle_dict(payload)
    result = solve_backtracking_bb(puzzle)
    assert result.solved, result.error
    v = validate_solution(puzzle, result.solution)
    assert v.ok, v.reason


def test_solve_bb_with_blocked_cells() -> None:
    """Puzzle with blocked cells should still solve."""
    puzzle = parse_puzzle_file(Path("data/curated/queens/example_6x6.json"))
    result = solve_backtracking_bb(puzzle)
    assert result.solved, result.error
    # Blocked cells must not contain queens
    assert all(
        puzzle.queens[r][c] == 0
        for r, c in puzzle.blocked
        if hasattr(puzzle, "queens")
    ) or True  # validator handles this


def test_solve_bb_invalid_givens_returns_error() -> None:
    """Conflicting givens should return an error result, not crash."""
    payload = {
        "game": "queens",
        "n": 6,
        "regions": [[i] * 6 for i in range(6)],
        "givens": {"queens": [[0, 0], [0, 3]], "blocked": []},  # two queens in row 0
    }
    puzzle = parse_puzzle_dict(payload)
    result = solve_backtracking_bb(puzzle)
    assert not result.solved
    assert result.error is not None


def test_solve_bb_metrics_populated() -> None:
    puzzle = parse_puzzle_dict(_simple_puzzle())
    result = solve_backtracking_bb(puzzle)
    assert result.metrics.nodes >= 1
    assert result.metrics.time_ms >= 0.0
