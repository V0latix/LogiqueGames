"""Tests for Queens and Zip solver registries."""

from __future__ import annotations

import pytest

from linkedin_game_solver.games.queens.parser import parse_puzzle_dict as parse_queens
from linkedin_game_solver.games.queens.solvers import get_solver as get_queens_solver, list_solvers as list_queens_solvers
from linkedin_game_solver.games.zip.parser import parse_puzzle_dict as parse_zip
from linkedin_game_solver.games.zip.solvers import get_solver as get_zip_solver, list_solvers as list_zip_solvers


def _queens_puzzle() -> object:
    return parse_queens({
        "game": "queens",
        "n": 6,
        "regions": [[i] * 6 for i in range(6)],
        "givens": {"queens": [], "blocked": []},
    })


def _zip_puzzle() -> object:
    return parse_zip({
        "game": "zip",
        "n": 4,
        "numbers": [{"k": 1, "r": 0, "c": 0}, {"k": 2, "r": 3, "c": 3}],
        "walls": [],
    })


# ── Queens registry ──────────────────────────────────────────────────────────

def test_queens_list_solvers_returns_all() -> None:
    solvers = list_queens_solvers()
    assert "backtracking_bb" in solvers
    assert "backtracking_bb_nolcv" in solvers
    assert "baseline" in solvers
    assert "heuristic_simple" in solvers
    assert "heuristic_lcv" in solvers
    assert "dlx" in solvers
    assert "csp_ac3" in solvers
    assert len(solvers) == 7


def test_queens_get_solver_valid() -> None:
    solver = get_queens_solver("baseline")
    puzzle = _queens_puzzle()
    result = solver(puzzle, None)
    assert result.solved


def test_queens_get_solver_backtracking_bb() -> None:
    solver = get_queens_solver("backtracking_bb")
    puzzle = _queens_puzzle()
    result = solver(puzzle, None)
    assert result.solved


def test_queens_get_solver_backtracking_bb_nolcv() -> None:
    solver = get_queens_solver("backtracking_bb_nolcv")
    puzzle = _queens_puzzle()
    result = solver(puzzle, None)
    assert result.solved


def test_queens_get_solver_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unknown queens solver"):
        get_queens_solver("does_not_exist")


# ── Zip registry ─────────────────────────────────────────────────────────────

def test_zip_list_solvers_returns_all() -> None:
    solvers = list_zip_solvers()
    assert "baseline" in solvers
    assert "forced" in solvers
    assert "articulation" in solvers
    assert "heuristic" in solvers
    assert "heuristic_nolcv" in solvers
    assert len(solvers) == 5


def test_zip_get_solver_valid() -> None:
    solver = get_zip_solver("baseline")
    puzzle = _zip_puzzle()
    result = solver(puzzle, 1.0)
    assert result.solved


def test_zip_get_solver_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unknown zip solver"):
        get_zip_solver("does_not_exist")
