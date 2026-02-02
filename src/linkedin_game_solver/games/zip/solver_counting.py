"""Backtracking solution counter for Zip."""

from __future__ import annotations

import time
from dataclasses import dataclass

from .model import Cell, ZipPuzzle


@dataclass
class CountResult:
    solutions: int
    timed_out: bool


def _free_neighbors(puzzle: ZipPuzzle, visited: set[Cell], cell: Cell) -> list[Cell]:
    return [nbr for nbr in puzzle.neighbors[cell] if nbr not in visited]


def _isolated_cells(puzzle: ZipPuzzle, visited: set[Cell], current: Cell) -> bool:
    unvisited = []
    for r in range(puzzle.n):
        for c in range(puzzle.n):
            cell = (r, c)
            if cell not in visited:
                unvisited.append(cell)
    if not unvisited:
        return False

    remaining = len(unvisited)
    for cell in unvisited:
        if _free_neighbors(puzzle, visited, cell):
            continue
        if remaining == 1 and current in puzzle.neighbors[cell]:
            continue
        return True
    return False


def _components_ok(puzzle: ZipPuzzle, visited: set[Cell]) -> bool:
    unvisited = {(r, c) for r in range(puzzle.n) for c in range(puzzle.n) if (r, c) not in visited}
    if not unvisited:
        return True
    stack = [next(iter(unvisited))]
    seen = {stack[0]}
    while stack:
        cell = stack.pop()
        for nxt in puzzle.neighbors[cell]:
            if nxt in unvisited and nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen == unvisited


def _lcv_score(puzzle: ZipPuzzle, visited: set[Cell], candidate: Cell) -> int:
    score = 0
    for neighbor in _free_neighbors(puzzle, visited, candidate):
        score += len(_free_neighbors(puzzle, visited, neighbor))
    return score


def count_solutions(
    puzzle: ZipPuzzle,
    time_limit_s: float | None = None,
    max_solutions: int = 2,
) -> CountResult:
    if 1 not in puzzle.numbers:
        return CountResult(solutions=0, timed_out=False)

    start_time = time.perf_counter()
    limit_ms = None if time_limit_s is None else max(0.0, time_limit_s * 1000.0)

    def timed_out() -> bool:
        if limit_ms is None:
            return False
        return (time.perf_counter() - start_time) * 1000.0 >= limit_ms

    start = puzzle.numbers[1]
    max_k = max(puzzle.numbers.keys())
    next_k = 2 if max_k >= 2 else max_k + 1

    path: list[Cell] = [start]
    visited = {start}
    solutions = 0

    def is_checkpoint(cell: Cell) -> int | None:
        for k, pos in puzzle.numbers.items():
            if pos == cell:
                return k
        return None

    def dfs(current: Cell, next_target: int) -> bool:
        nonlocal solutions
        if timed_out():
            return False
        if len(path) == puzzle.n * puzzle.n:
            solutions += 1
            return solutions < max_solutions
        if _isolated_cells(puzzle, visited, current):
            return True
        if not _components_ok(puzzle, visited):
            return True

        neighbors = _free_neighbors(puzzle, visited, current)
        if not neighbors:
            return True

        neighbors.sort(
            key=lambda cell: (
                -_lcv_score(puzzle, visited, cell),
                len(_free_neighbors(puzzle, visited, cell)),
            )
        )

        for nxt in neighbors:
            if timed_out():
                return False
            k = is_checkpoint(nxt)
            if k is not None and k != next_target:
                continue
            next_for_child = next_target
            if k is not None:
                next_for_child += 1

            visited.add(nxt)
            path.append(nxt)
            cont = dfs(nxt, next_for_child)
            path.pop()
            visited.remove(nxt)
            if not cont:
                return False
            if solutions >= max_solutions:
                return False
        return True

    dfs(start, next_k)
    return CountResult(solutions=solutions, timed_out=timed_out())
