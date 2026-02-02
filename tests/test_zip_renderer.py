from __future__ import annotations

from linkedin_game_solver.games.zip.model import ZipSolution
from linkedin_game_solver.games.zip.parser import parse_puzzle_file
from linkedin_game_solver.games.zip.renderer import render_puzzle, render_solution


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


def test_render_zip_puzzle() -> None:
    puzzle = parse_puzzle_file("data/curated/zip/zip_n4_01.json")
    rendered = render_puzzle(puzzle).text
    assert "game=zip" in rendered
    assert "numbers:" in rendered


def test_render_zip_solution() -> None:
    puzzle = parse_puzzle_file("data/curated/zip/zip_n4_01.json")
    solution = ZipSolution(path=_snake_path_4())
    rendered = render_solution(puzzle, solution).text
    assert "order" in rendered
    assert "path:" in rendered
