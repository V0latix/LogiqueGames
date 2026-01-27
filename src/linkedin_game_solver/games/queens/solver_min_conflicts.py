"""Min-Conflicts local search solver for the LinkedIn Queens puzzle."""

from __future__ import annotations

import random
from dataclasses import dataclass

from ...core.metrics import Timer
from ...core.types import SolveMetrics, SolveResult
from .parser import Cell, QueensPuzzle, QueensSolution
from .validator import validate_solution


@dataclass
class _State:
    assignment: list[int]
    col_counts: list[int]
    region_counts: dict[int, int]
    positions: set[Cell]


def _adjacent(a: Cell, b: Cell) -> bool:
    ar, ac = a
    br, bc = b
    return max(abs(ar - br), abs(ac - bc)) <= 1


def _region_id(puzzle: QueensPuzzle, r: int, c: int) -> int:
    return puzzle.regions[r][c]


def _build_initial_state(puzzle: QueensPuzzle, rng: random.Random) -> _State:
    n = puzzle.n
    assignment = [-1 for _ in range(n)]
    col_counts = [0 for _ in range(n)]
    region_counts: dict[int, int] = {region_id: 0 for region_id in puzzle.region_ids}
    positions: set[Cell] = set()

    blocked_by_row: dict[int, set[int]] = {r: set() for r in range(n)}
    for r, c in puzzle.blocked:
        blocked_by_row[r].add(c)

    given_by_row: dict[int, int] = {}
    for r, c in puzzle.givens_queens:
        if r in given_by_row and given_by_row[r] != c:
            msg = f"multiple given queens in row {r}"
            raise ValueError(msg)
        given_by_row[r] = c

    for r in range(n):
        if r in given_by_row:
            c = given_by_row[r]
            if c in blocked_by_row[r]:
                msg = "given queen is on a blocked cell"
                raise ValueError(msg)
        else:
            candidates = [c for c in range(n) if c not in blocked_by_row[r]]
            if not candidates:
                msg = f"row {r} has no available columns"
                raise ValueError(msg)
            c = rng.choice(candidates)

        assignment[r] = c
        col_counts[c] += 1
        region_counts[_region_id(puzzle, r, c)] += 1
        positions.add((r, c))

    return _State(
        assignment=assignment,
        col_counts=col_counts,
        region_counts=region_counts,
        positions=positions,
    )


def _conflicts_for(puzzle: QueensPuzzle, state: _State, row: int, col: int) -> int:
    conflicts = 0

    if state.col_counts[col] > 0:
        conflicts += state.col_counts[col]
        if state.assignment[row] == col:
            conflicts -= 1

    region_id = _region_id(puzzle, row, col)
    if state.region_counts[region_id] > 0:
        conflicts += state.region_counts[region_id]
        if state.assignment[row] == col:
            conflicts -= 1

    for r, c in state.positions:
        if r == row and c == col:
            continue
        if _adjacent((row, col), (r, c)):
            conflicts += 1

    return conflicts


def _most_conflicted_rows(puzzle: QueensPuzzle, state: _State) -> list[int]:
    conflicts_by_row: list[tuple[int, int]] = []
    for r, c in enumerate(state.assignment):
        conflicts = _conflicts_for(puzzle, state, r, c)
        conflicts_by_row.append((conflicts, r))

    max_conflicts = max(conflicts_by_row, key=lambda item: item[0])[0]
    if max_conflicts == 0:
        return []

    return [r for conflicts, r in conflicts_by_row if conflicts == max_conflicts]


def _best_columns(puzzle: QueensPuzzle, state: _State, row: int) -> list[int]:
    blocked_cols = {c for (rr, c) in puzzle.blocked if rr == row}
    candidates = [c for c in range(puzzle.n) if c not in blocked_cols]

    best: list[int] = []
    best_score: int | None = None
    for col in candidates:
        score = _conflicts_for(puzzle, state, row, col)
        if best_score is None or score < best_score:
            best_score = score
            best = [col]
        elif score == best_score:
            best.append(col)

    return best


def _move_queen(puzzle: QueensPuzzle, state: _State, row: int, new_col: int) -> None:
    old_col = state.assignment[row]
    if old_col == new_col:
        return

    state.positions.remove((row, old_col))
    state.col_counts[old_col] -= 1
    old_region = _region_id(puzzle, row, old_col)
    state.region_counts[old_region] -= 1

    state.assignment[row] = new_col
    state.positions.add((row, new_col))
    state.col_counts[new_col] += 1
    new_region = _region_id(puzzle, row, new_col)
    state.region_counts[new_region] += 1


def solve_min_conflicts(
    puzzle: QueensPuzzle,
    time_limit_s: float | None = None,
    max_steps: int = 5000,
    restarts: int = 20,
    seed: int | None = None,
) -> SolveResult:
    """Solve Queens using Min-Conflicts local search.

    Picks the most conflicted row and moves it to a column minimizing conflicts.
    Uses random tie-breaking and random restarts for robustness.
    """

    timer = Timer()
    timer.start()
    metrics = SolveMetrics()
    limit_ms = None if time_limit_s is None else max(0.0, time_limit_s * 1000.0)

    rng = random.Random(seed)

    def timed_out() -> bool:
        return limit_ms is not None and timer.elapsed_ms() >= limit_ms

    for _restart in range(restarts + 1):
        try:
            state = _build_initial_state(puzzle, rng)
        except ValueError as exc:
            metrics.time_ms = timer.elapsed_ms()
            return SolveResult(
                solved=False,
                solution=None,
                metrics=metrics,
                error=f"Invalid puzzle givens: {exc}",
            )

        for _ in range(max_steps):
            if timed_out():
                metrics.time_ms = timer.elapsed_ms()
                return SolveResult(
                    solved=False,
                    solution=None,
                    metrics=metrics,
                    error="Timeout: solver exceeded the time limit.",
                )

            conflicted_rows = _most_conflicted_rows(puzzle, state)
            if not conflicted_rows:
                queens = [[0 for _ in range(puzzle.n)] for _ in range(puzzle.n)]
                for r, c in enumerate(state.assignment):
                    queens[r][c] = 1
                solution = QueensSolution(queens=queens)
                validation = validate_solution(puzzle, solution)
                if not validation.ok:
                    metrics.time_ms = timer.elapsed_ms()
                    return SolveResult(
                        solved=False,
                        solution=None,
                        metrics=metrics,
                        error=f"Solver produced an invalid solution: {validation.reason}",
                    )
                metrics.time_ms = timer.elapsed_ms()
                return SolveResult(solved=True, solution=solution, metrics=metrics, error=None)

            row = rng.choice(conflicted_rows)
            best_cols = _best_columns(puzzle, state, row)
            new_col = rng.choice(best_cols)
            _move_queen(puzzle, state, row, new_col)
            metrics.nodes += 1

        metrics.backtracks += 1

    metrics.time_ms = timer.elapsed_ms()
    return SolveResult(
        solved=False,
        solution=None,
        metrics=metrics,
        error="No solution found within restart/step limits.",
    )
