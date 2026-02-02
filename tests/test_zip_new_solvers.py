from __future__ import annotations

from linkedin_game_solver.games.zip.parser import parse_puzzle_file
from linkedin_game_solver.games.zip.solver_articulation import solve_articulation
from linkedin_game_solver.games.zip.solver_forced import solve_forced
from linkedin_game_solver.games.zip.validator import validate_solution


def test_zip_forced_solves_curated() -> None:
    puzzle = parse_puzzle_file("data/curated/zip/zip_n4_01.json")
    result = solve_forced(puzzle, time_limit_s=1.0)
    assert result.solved, result.error
    assert result.solution is not None
    validation = validate_solution(puzzle, result.solution)
    assert validation.ok, validation.reason


def test_zip_articulation_solves_curated() -> None:
    puzzle = parse_puzzle_file("data/curated/zip/zip_n4_01.json")
    result = solve_articulation(puzzle, time_limit_s=1.0)
    assert result.solved, result.error
    assert result.solution is not None
    validation = validate_solution(puzzle, result.solution)
    assert validation.ok, validation.reason
