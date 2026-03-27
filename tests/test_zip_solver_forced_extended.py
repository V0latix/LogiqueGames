"""Extended coverage tests for zip solver_forced."""

from __future__ import annotations

from linkedin_game_solver.games.zip.parser import parse_puzzle_dict
from linkedin_game_solver.games.zip.solver_forced import solve_forced
from linkedin_game_solver.games.zip.validator import validate_solution


def _puzzle(n: int, numbers: list[dict], walls: list[dict] | None = None) -> object:
    return parse_puzzle_dict({
        "game": "zip",
        "n": n,
        "numbers": numbers,
        "walls": walls or [],
    })


def test_solve_forced_2x2() -> None:
    puzzle = _puzzle(2, [{"k": 1, "r": 0, "c": 0}, {"k": 2, "r": 1, "c": 1}])
    result = solve_forced(puzzle, time_limit_s=1.0)
    assert result.solved, result.error
    v = validate_solution(puzzle, result.solution)
    assert v.ok, v.reason


def test_solve_forced_3x3() -> None:
    puzzle = _puzzle(3, [
        {"k": 1, "r": 0, "c": 0},
        {"k": 2, "r": 1, "c": 1},
        {"k": 3, "r": 2, "c": 2},
    ])
    result = solve_forced(puzzle, time_limit_s=1.0)
    assert result.solved, result.error
    v = validate_solution(puzzle, result.solution)
    assert v.ok, v.reason


def test_solve_forced_4x4_with_walls() -> None:
    """4x4 with some walls — exercises forced propagation."""
    puzzle = _puzzle(
        4,
        [{"k": 1, "r": 0, "c": 0}, {"k": 2, "r": 3, "c": 3}],
        walls=[
            {"r1": 0, "c1": 1, "r2": 1, "c2": 1},
            {"r1": 1, "c1": 2, "r2": 2, "c2": 2},
        ],
    )
    result = solve_forced(puzzle, time_limit_s=1.0)
    assert result.solved, result.error
    v = validate_solution(puzzle, result.solution)
    assert v.ok, v.reason


def test_solve_forced_time_limit_does_not_crash() -> None:
    puzzle = _puzzle(4, [
        {"k": 1, "r": 0, "c": 0},
        {"k": 2, "r": 3, "c": 3},
    ])
    result = solve_forced(puzzle, time_limit_s=0.000001)
    assert isinstance(result.solved, bool)


def test_solve_forced_only_k1() -> None:
    """Puzzle with only k=1 (no further checkpoints)."""
    puzzle = _puzzle(2, [{"k": 1, "r": 0, "c": 0}])
    result = solve_forced(puzzle, time_limit_s=1.0)
    assert result.solved, result.error


def test_solve_forced_metrics_populated() -> None:
    puzzle = _puzzle(3, [
        {"k": 1, "r": 0, "c": 0},
        {"k": 2, "r": 2, "c": 2},
    ])
    result = solve_forced(puzzle, time_limit_s=1.0)
    assert result.metrics.time_ms >= 0.0
    assert result.metrics.nodes >= 1


def test_solve_forced_missing_k1_returns_error() -> None:
    """Puzzle without k=1 should return an error result."""
    from linkedin_game_solver.games.zip.model import ZipPuzzle
    # Bypass parser to create a puzzle with no k=1 in numbers
    puzzle = ZipPuzzle(
        game="zip",
        n=2,
        numbers={2: (1, 1)},
        walls=set(),
        neighbors={(0, 0): [(1, 0), (0, 1)], (0, 1): [(0, 0), (1, 1)],
                   (1, 0): [(0, 0), (1, 1)], (1, 1): [(1, 0), (0, 1)]},
    )
    result = solve_forced(puzzle, time_limit_s=1.0)
    assert not result.solved
    assert result.error is not None
    assert "number 1" in result.error


def test_solve_forced_no_solution() -> None:
    """Puzzle with walls that make it unsolvable returns not-solved."""
    # 3x3 with walls isolating corner cells so no Hamiltonian path exists.
    # Wall between (0,0)-(0,1) and (0,0)-(1,0) leaves (0,0) with degree 0 → impossible.
    puzzle = _puzzle(
        3,
        [{"k": 1, "r": 0, "c": 0}, {"k": 2, "r": 2, "c": 2}],
        walls=[
            {"r1": 0, "c1": 0, "r2": 0, "c2": 1},
            {"r1": 0, "c1": 0, "r2": 1, "c2": 0},
        ],
    )
    result = solve_forced(puzzle, time_limit_s=2.0)
    assert not result.solved
