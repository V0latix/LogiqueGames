from __future__ import annotations

from linkedin_game_solver.games.zip.model import ZipSolution
from linkedin_game_solver.games.zip.parser import parse_puzzle_file
from linkedin_game_solver.games.zip.validator import validate_solution


def _snake_path_4() -> list[tuple[int, int]]:
    return [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 3),
        (1, 2),
        (1, 1),
        (1, 0),
        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),
        (3, 3),
        (3, 2),
        (3, 1),
        (3, 0),
    ]


def test_validate_solution_ok() -> None:
    puzzle = parse_puzzle_file("data/curated/zip/zip_n4_01.json")
    solution = ZipSolution(path=_snake_path_4())
    result = validate_solution(puzzle, solution)
    assert result.ok, result.reason


def test_validate_solution_bad_order() -> None:
    puzzle = parse_puzzle_file("data/curated/zip/zip_n4_01.json")
    path = _snake_path_4()
    path[0], path[5] = path[5], path[0]
    solution = ZipSolution(path=path)
    result = validate_solution(puzzle, solution)
    assert not result.ok
