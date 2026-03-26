"""Extended tests for the Queens generator — coverage of region modes and edge cases."""

from __future__ import annotations

import pytest

from linkedin_game_solver.games.queens.generator import (
    generate_puzzle,
    generate_puzzle_payload,
    generate_regions_from_solution,
    generate_solution,
)
from linkedin_game_solver.games.queens.parser import parse_puzzle_dict
from linkedin_game_solver.games.queens.validator import validate_solution


# ── generate_solution ────────────────────────────────────────────────────────

def test_generate_solution_n4() -> None:
    sol = generate_solution(4, seed=0)
    positions = sol.positions()
    assert len(positions) == 4
    rows = {r for r, _ in positions}
    cols = {c for _, c in positions}
    assert rows == {0, 1, 2, 3}
    assert cols == {0, 1, 2, 3}


def test_generate_solution_n8() -> None:
    sol = generate_solution(8, seed=1)
    assert len(sol.positions()) == 8


# ── generate_regions_from_solution — all modes ───────────────────────────────

def test_generate_regions_balanced() -> None:
    sol = generate_solution(6, seed=5)
    regions = generate_regions_from_solution(sol, seed=5, mode="balanced")
    assert len(regions) == 6
    assert len(regions[0]) == 6


def test_generate_regions_serpentine() -> None:
    sol = generate_solution(6, seed=5)
    regions = generate_regions_from_solution(sol, seed=5, mode="serpentine")
    # All cells assigned
    assigned = {regions[r][c] for r in range(6) for c in range(6)}
    assert len(assigned) == 6


def test_generate_regions_biased() -> None:
    sol = generate_solution(6, seed=3)
    regions = generate_regions_from_solution(sol, seed=3, mode="biased")
    assigned = {regions[r][c] for r in range(6) for c in range(6)}
    assert len(assigned) == 6


def test_generate_regions_constrained() -> None:
    sol = generate_solution(6, seed=2)
    regions = generate_regions_from_solution(sol, seed=2, mode="constrained")
    assigned = {regions[r][c] for r in range(6) for c in range(6)}
    assert len(assigned) == 6


# ── generate_puzzle_payload — various options ─────────────────────────────────

def test_generate_payload_ensure_unique_false() -> None:
    payload, solution = generate_puzzle_payload(6, seed=7, ensure_unique=False)
    puzzle = parse_puzzle_dict(payload)
    v = validate_solution(puzzle, solution)
    assert v.ok, v.reason


def test_generate_payload_repair_steps() -> None:
    payload, solution = generate_puzzle_payload(
        6, seed=5, ensure_unique=False, repair_steps=3, block_steps=0
    )
    puzzle = parse_puzzle_dict(payload)
    v = validate_solution(puzzle, solution)
    assert v.ok, v.reason


def test_generate_payload_block_steps() -> None:
    payload, solution = generate_puzzle_payload(
        6, seed=5, ensure_unique=False, block_steps=3
    )
    puzzle = parse_puzzle_dict(payload)
    v = validate_solution(puzzle, solution)
    assert v.ok, v.reason


def test_generate_payload_region_mode_serpentine() -> None:
    payload, solution = generate_puzzle_payload(
        6, seed=1, ensure_unique=False, region_mode="serpentine"
    )
    puzzle = parse_puzzle_dict(payload)
    v = validate_solution(puzzle, solution)
    assert v.ok, v.reason


def test_generate_payload_region_mode_biased() -> None:
    payload, solution = generate_puzzle_payload(
        6, seed=2, ensure_unique=False, region_mode="biased"
    )
    puzzle = parse_puzzle_dict(payload)
    v = validate_solution(puzzle, solution)
    assert v.ok, v.reason


def test_generate_payload_region_mode_constrained() -> None:
    payload, solution = generate_puzzle_payload(
        6, seed=3, ensure_unique=False, region_mode="constrained"
    )
    puzzle = parse_puzzle_dict(payload)
    v = validate_solution(puzzle, solution)
    assert v.ok, v.reason


def test_generate_payload_region_mode_mixed() -> None:
    payload, solution = generate_puzzle_payload(
        6, seed=4, ensure_unique=False, region_mode="mixed"
    )
    puzzle = parse_puzzle_dict(payload)
    v = validate_solution(puzzle, solution)
    assert v.ok, v.reason


def test_generate_payload_max_attempts_exceeded_raises() -> None:
    with pytest.raises(ValueError, match="Unable to generate"):
        generate_puzzle_payload(6, seed=1, ensure_unique=True, max_attempts=1)


def test_generate_payload_invalid_selection_mode_raises() -> None:
    with pytest.raises(ValueError, match="unknown selection_mode"):
        generate_puzzle_payload(6, ensure_unique=False, selection_mode="invalid")


def test_generate_payload_invalid_region_mode_raises() -> None:
    with pytest.raises(ValueError, match="unknown region_mode"):
        generate_puzzle_payload(6, ensure_unique=False, region_mode="invalid")


def test_generate_payload_max_attempts_zero_raises() -> None:
    with pytest.raises(ValueError, match="max_attempts must be positive"):
        generate_puzzle_payload(6, max_attempts=0)


def test_generate_puzzle_returns_valid_object() -> None:
    gen = generate_puzzle(n=6, seed=11, ensure_unique=False)
    assert gen.puzzle is not None
    assert gen.solution is not None
    assert gen.payload is not None
    v = validate_solution(gen.puzzle, gen.solution)
    assert v.ok, v.reason


def test_generate_payload_selection_mode_best() -> None:
    payload, solution = generate_puzzle_payload(
        6, seed=1, ensure_unique=False,
        selection_mode="best", candidates=3, max_attempts=3
    )
    puzzle = parse_puzzle_dict(payload)
    v = validate_solution(puzzle, solution)
    assert v.ok, v.reason
