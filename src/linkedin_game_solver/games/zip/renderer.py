"""Console renderers for Zip puzzles and solutions."""

from __future__ import annotations

from dataclasses import dataclass

from .model import ZipPuzzle, ZipSolution


@dataclass
class Rendered:
    text: str


def _grid_to_text(grid: list[list[str]]) -> str:
    return "\n".join(" ".join(row) for row in grid)


def render_puzzle(puzzle: ZipPuzzle) -> Rendered:
    n = puzzle.n
    grid = [["." for _ in range(n)] for _ in range(n)]
    for k, (r, c) in puzzle.numbers.items():
        grid[r][c] = str(k)
    header = f"game=zip n={n} numbers={len(puzzle.numbers)} walls={len(puzzle.walls)}"
    body = _grid_to_text(grid)
    numbers = " ".join(f"{k}:({r},{c})" for k, (r, c) in sorted(puzzle.numbers.items()))
    return Rendered(text=f"{header}\n{body}\n\nnumbers: {numbers}")


def render_solution(puzzle: ZipPuzzle, solution: ZipSolution) -> Rendered:
    n = puzzle.n
    order = solution.order_grid(n)
    width = len(str(n * n - 1))
    grid = [[str(order[r][c]).rjust(width) for c in range(n)] for r in range(n)]
    header = render_puzzle(puzzle).text
    body = _grid_to_text(grid)
    path = " ".join(f"({r},{c})" for r, c in solution.path)
    return Rendered(text=f"{header}\n\norder\n{body}\n\npath: [{path}]")
