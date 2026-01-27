"""CSP + AC-3 solver for the LinkedIn Queens puzzle."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from ...core.metrics import Timer
from ...core.types import SolveMetrics, SolveResult
from .parser import Cell, QueensPuzzle, QueensSolution
from .validator import validate_solution


@dataclass
class _CSPState:
    domains: dict[int, set[int]]
    assignment: dict[int, int]


def _adjacent(a: Cell, b: Cell) -> bool:
    ar, ac = a
    br, bc = b
    return max(abs(ar - br), abs(ac - bc)) <= 1


def _build_initial_domains(puzzle: QueensPuzzle) -> _CSPState:
    n = puzzle.n
    domains: dict[int, set[int]] = {}
    assignment: dict[int, int] = {}

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
            domains[r] = {c}
            assignment[r] = c
        else:
            domains[r] = {c for c in range(n) if c not in blocked_by_row[r]}

        if not domains[r]:
            msg = f"row {r} has no available columns"
            raise ValueError(msg)

    return _CSPState(domains=domains, assignment=assignment)


def _region_id(puzzle: QueensPuzzle, r: int, c: int) -> int:
    return puzzle.regions[r][c]


def _consistent(
    puzzle: QueensPuzzle,
    row_a: int,
    col_a: int,
    row_b: int,
    col_b: int,
) -> bool:
    if col_a == col_b:
        return False
    if _region_id(puzzle, row_a, col_a) == _region_id(puzzle, row_b, col_b):
        return False
    return not _adjacent((row_a, col_a), (row_b, col_b))


def _ac3(puzzle: QueensPuzzle, state: _CSPState) -> bool:
    queue: deque[tuple[int, int]] = deque()
    rows = list(state.domains)
    for i in rows:
        for j in rows:
            if i != j:
                queue.append((i, j))

    while queue:
        xi, xj = queue.popleft()
        if _revise(puzzle, state, xi, xj):
            if not state.domains[xi]:
                return False
            for xk in rows:
                if xk != xi and xk != xj:
                    queue.append((xk, xi))
    return True


def _revise(puzzle: QueensPuzzle, state: _CSPState, xi: int, xj: int) -> bool:
    revised = False
    to_remove = set()
    for vi in state.domains[xi]:
        if not any(_consistent(puzzle, xi, vi, xj, vj) for vj in state.domains[xj]):
            to_remove.add(vi)
    if to_remove:
        state.domains[xi] -= to_remove
        revised = True
    return revised


def _select_row_mrv(state: _CSPState) -> int | None:
    unassigned = [r for r in state.domains if r not in state.assignment]
    if not unassigned:
        return None
    return min(unassigned, key=lambda r: len(state.domains[r]))


def _order_values_lcv(puzzle: QueensPuzzle, state: _CSPState, row: int) -> list[int]:
    scores: list[tuple[int, int]] = []
    for col in state.domains[row]:
        score = 0
        for other_row in state.domains:
            if other_row == row:
                continue
            score += sum(
                1
                for other_col in state.domains[other_row]
                if not _consistent(puzzle, row, col, other_row, other_col)
            )
        scores.append((score, col))
    scores.sort(key=lambda item: (item[0], item[1]))
    return [col for _, col in scores]


def _deep_copy_state(state: _CSPState) -> _CSPState:
    return _CSPState(
        domains={row: set(values) for row, values in state.domains.items()},
        assignment=dict(state.assignment),
    )


def solve_csp_ac3(puzzle: QueensPuzzle, time_limit_s: float | None = None) -> SolveResult:
    """Solve Queens using CSP + AC-3 + MRV + LCV.

    AC-3 ensures arc consistency between rows, then backtracking assigns rows
    using MRV and LCV to prune the search efficiently.
    """

    timer = Timer()
    timer.start()
    metrics = SolveMetrics()
    limit_ms = None if time_limit_s is None else max(0.0, time_limit_s * 1000.0)

    try:
        state = _build_initial_domains(puzzle)
    except ValueError as exc:
        metrics.time_ms = timer.elapsed_ms()
        return SolveResult(
            solved=False,
            solution=None,
            metrics=metrics,
            error=f"Invalid puzzle givens: {exc}",
        )

    if not _ac3(puzzle, state):
        metrics.time_ms = timer.elapsed_ms()
        return SolveResult(
            solved=False,
            solution=None,
            metrics=metrics,
            error="No solution found after AC-3 pruning.",
        )

    def timed_out() -> bool:
        return limit_ms is not None and timer.elapsed_ms() >= limit_ms

    def backtrack(current: _CSPState) -> bool | None:
        if timed_out():
            return None

        row = _select_row_mrv(current)
        if row is None:
            return True

        for col in _order_values_lcv(puzzle, current, row):
            if timed_out():
                return None
            metrics.nodes += 1
            new_state = _deep_copy_state(current)
            new_state.assignment[row] = col
            new_state.domains[row] = {col}

            if _ac3(puzzle, new_state):
                result = backtrack(new_state)
                if result is None:
                    return None
                if result:
                    current.assignment = new_state.assignment
                    current.domains = new_state.domains
                    return True

            metrics.backtracks += 1

        return False

    solved = backtrack(state)
    metrics.time_ms = timer.elapsed_ms()

    if solved is None:
        return SolveResult(
            solved=False,
            solution=None,
            metrics=metrics,
            error="Timeout: solver exceeded the time limit.",
        )
    if not solved:
        return SolveResult(
            solved=False,
            solution=None,
            metrics=metrics,
            error="No solution found under the given constraints.",
        )

    queens = [[0 for _ in range(puzzle.n)] for _ in range(puzzle.n)]
    for r, c in state.assignment.items():
        queens[r][c] = 1

    solution = QueensSolution(queens=queens)
    validation = validate_solution(puzzle, solution)
    if not validation.ok:
        return SolveResult(
            solved=False,
            solution=None,
            metrics=metrics,
            error=f"Solver produced an invalid solution: {validation.reason}",
        )

    return SolveResult(solved=True, solution=solution, metrics=metrics, error=None)
