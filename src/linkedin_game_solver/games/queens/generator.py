"""Puzzle generator for the LinkedIn Queens puzzle (educational, v1)."""

from __future__ import annotations

import random
from collections.abc import Iterable
from dataclasses import dataclass

from .parser import Cell, Grid, QueensPuzzle, QueensSolution, parse_puzzle_dict
from .solver_dlx import count_solutions_dlx
from .validator import validate_solution


@dataclass
class GeneratedPuzzle:
    """Container for a generated puzzle and its known-valid solution."""

    puzzle: QueensPuzzle
    solution: QueensSolution
    payload: dict


def _adjacent(a: Cell, b: Cell) -> bool:
    ar, ac = a
    br, bc = b
    return max(abs(ar - br), abs(ac - bc)) <= 1


def _matrix_from_positions(n: int, positions: Iterable[Cell]) -> list[list[int]]:
    grid = [[0 for _ in range(n)] for _ in range(n)]
    for r, c in positions:
        grid[r][c] = 1
    return grid


def generate_solution(n: int, seed: int | None = None) -> QueensSolution:
    """Generate a valid queens placement (row/col + non-adjacency).

    Intuition: backtrack row by row, enforcing column uniqueness and the
    official non-adjacency constraint. Worst-case complexity is exponential,
    but it works well for small/medium sizes and is good enough for v1.
    """

    rng = random.Random(seed)
    cols_used: set[int] = set()
    positions: list[Cell] = []

    def can_place(r: int, c: int) -> bool:
        if c in cols_used:
            return False
        return all(not _adjacent((r, c), pos) for pos in positions)

    def dfs(row: int) -> bool:
        if row == n:
            return True

        candidates = list(range(n))
        rng.shuffle(candidates)
        for col in candidates:
            if not can_place(row, col):
                continue
            cols_used.add(col)
            positions.append((row, col))
            if dfs(row + 1):
                return True
            positions.pop()
            cols_used.remove(col)
        return False

    if not dfs(0):
        msg = f"Unable to generate a valid solution for n={n}"
        raise ValueError(msg)

    return QueensSolution(queens=_matrix_from_positions(n, positions))


def _neighbors4(n: int, r: int, c: int) -> list[Cell]:
    candidates = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    return [(rr, cc) for rr, cc in candidates if 0 <= rr < n and 0 <= cc < n]


def generate_regions_from_solution(
    solution: QueensSolution,
    seed: int | None = None,
) -> Grid:
    """Build a region partition compatible with the given solution.

    Strategy: use each queen cell as a seed and grow regions via random
    multi-source expansion until the full grid is covered. This guarantees
    exactly one queen per region because each region has a single seed.
    """

    rng = random.Random(seed)
    n = len(solution.queens)
    positions = solution.positions()
    if len(positions) != n:
        msg = "solution must contain exactly n queens to seed n regions"
        raise ValueError(msg)

    region_by_cell: list[list[int]] = [[-1 for _ in range(n)] for _ in range(n)]
    frontiers: dict[int, set[Cell]] = {}
    region_sizes: dict[int, int] = {}

    for region_id, (r, c) in enumerate(sorted(positions)):
        region_by_cell[r][c] = region_id
        frontiers[region_id] = set(_neighbors4(n, r, c))
        region_sizes[region_id] = 1

    unassigned = {(r, c) for r in range(n) for c in range(n) if region_by_cell[r][c] < 0}

    while unassigned:
        expandable = [rid for rid, frontier in frontiers.items() if frontier & unassigned]
        if not expandable:
            # Fallback: attach a remaining cell to the nearest region by Manhattan distance.
            r, c = next(iter(unassigned))
            best_region = min(
                region_sizes,
                key=lambda rid: min(abs(r - rr) + abs(c - cc) for rr, cc in positions if region_by_cell[rr][cc] == rid),
            )
            region_by_cell[r][c] = best_region
            region_sizes[best_region] += 1
            unassigned.remove((r, c))
            frontiers[best_region].update(_neighbors4(n, r, c))
            continue

        # Prefer smaller regions to keep the partition reasonably balanced.
        min_size = min(region_sizes[rid] for rid in expandable)
        smallest = [rid for rid in expandable if region_sizes[rid] == min_size]
        region_id = rng.choice(smallest)

        candidates = list(frontiers[region_id] & unassigned)
        rng.shuffle(candidates)
        r, c = candidates[0]

        region_by_cell[r][c] = region_id
        region_sizes[region_id] += 1
        unassigned.remove((r, c))
        frontiers[region_id].update(_neighbors4(n, r, c))

    return region_by_cell


def _generate_payload_once(n: int, seed: int | None) -> tuple[dict, QueensSolution]:
    solution = generate_solution(n, seed=seed)
    regions = generate_regions_from_solution(solution, seed=seed)
    payload = {
        "game": "queens",
        "n": n,
        "regions": regions,
        "givens": {"queens": [], "blocked": []},
    }
    return payload, solution


def _is_unique_payload(payload: dict, time_limit_s: float | None) -> bool:
    puzzle = parse_puzzle_dict(payload)
    count = count_solutions_dlx(puzzle, limit=2, time_limit_s=time_limit_s)
    return count == 1


def _with_givens(payload: dict, givens: list[Cell]) -> dict:
    return {
        "game": payload["game"],
        "n": payload["n"],
        "regions": payload["regions"],
        "givens": {
            "queens": [[r, c] for r, c in givens],
            "blocked": [],
        },
    }


def generate_puzzle_payload(
    n: int,
    seed: int | None = None,
    ensure_unique: bool = True,
    max_attempts: int = 50,
    time_limit_s: float | None = None,
) -> tuple[dict, QueensSolution]:
    """Generate a puzzle JSON payload plus its known-valid solution.

    When ensure_unique=True, the generator retries until the puzzle has exactly
    one solution (checked by DLX up to 2 solutions).
    """

    if max_attempts <= 0:
        msg = "max_attempts must be positive"
        raise ValueError(msg)

    rng = random.Random(seed)

    for attempt in range(max_attempts):
        attempt_seed = rng.randint(0, 10_000_000) if seed is None else seed + attempt

        base_payload, solution = _generate_payload_once(n, seed=attempt_seed)
        if not ensure_unique:
            return base_payload, solution

        payload = _with_givens(base_payload, [])
        if _is_unique_payload(payload, time_limit_s):
            return payload, solution

        positions = solution.positions()
        rng.shuffle(positions)
        givens: list[Cell] = []
        for pos in positions:
            givens.append(pos)
            payload = _with_givens(base_payload, givens)
            if _is_unique_payload(payload, time_limit_s):
                return payload, solution

    msg = f"Unable to generate a unique puzzle for n={n} after {max_attempts} attempts"
    raise ValueError(msg)


def generate_puzzle(
    n: int,
    seed: int | None = None,
    ensure_unique: bool = True,
    max_attempts: int = 50,
    time_limit_s: float | None = None,
) -> GeneratedPuzzle:
    """Generate a parsed puzzle along with its known-valid solution."""

    payload, solution = generate_puzzle_payload(
        n,
        seed=seed,
        ensure_unique=ensure_unique,
        max_attempts=max_attempts,
        time_limit_s=time_limit_s,
    )
    puzzle = parse_puzzle_dict(payload)
    validation = validate_solution(puzzle, solution)
    if not validation.ok:
        msg = f"generator produced an invalid (puzzle, solution) pair: {validation.reason}"
        raise ValueError(msg)
    return GeneratedPuzzle(puzzle=puzzle, solution=solution, payload=payload)
