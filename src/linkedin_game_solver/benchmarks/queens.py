"""Benchmark runner and Markdown reporting for the Queens puzzle."""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean

from linkedin_game_solver.core.types import SolveMetrics
from linkedin_game_solver.datasets.exporter import load_manifest
from linkedin_game_solver.games.queens.parser import (
    QueensPuzzle,
    parse_puzzle_dict,
    parse_puzzle_file,
)
from linkedin_game_solver.games.queens.solvers import get_solver, list_solvers


@dataclass
class BenchRow:
    puzzle_id: str
    algo: str
    solved: bool
    metrics: SolveMetrics
    error: str | None
    n: int
    source: str


@dataclass
class AlgoSummary:
    algo: str
    puzzles: int
    solved: int
    solve_rate: float
    avg_time_ms: float
    median_time_ms: float
    avg_nodes: float
    avg_backtracks: float


def _parse_algo_list(algo_csv: str) -> list[str]:
    names = [part.strip() for part in algo_csv.split(",") if part.strip()]
    if not names:
        msg = "No algorithms provided."
        raise ValueError(msg)
    for name in names:
        get_solver(name)
    return names


def _puzzle_id_from_path(path: Path) -> str:
    return path.stem


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return float(ordered[mid])
    return float((ordered[mid - 1] + ordered[mid]) / 2.0)


def _load_puzzles_from_manifest(path: Path, limit: int | None) -> list[tuple[str, QueensPuzzle, str]]:
    puzzles: list[tuple[str, QueensPuzzle, str]] = []
    entries = load_manifest(path)
    if limit is not None:
        entries = entries[:limit]
    for entry in entries:
        payload = {
            "game": "queens",
            "n": entry["n"],
            "regions": entry["regions"],
            "givens": entry.get("givens", {"queens": [], "blocked": []}),
        }
        puzzle = parse_puzzle_dict(payload)
        puzzle_id = f"manifest_{entry['id']}"
        source = entry.get("source", "unknown")
        puzzles.append((puzzle_id, puzzle, source))
    if not puzzles:
        msg = f"No puzzles found in manifest: {path}"
        raise ValueError(msg)
    return puzzles


def _load_puzzles(dataset_dir: Path, limit: int | None) -> list[tuple[str, QueensPuzzle, str]]:
    if dataset_dir.is_file():
        return _load_puzzles_from_manifest(dataset_dir, limit=limit)

    if not dataset_dir.exists():
        msg = f"Dataset directory does not exist: {dataset_dir}"
        raise ValueError(msg)

    paths = sorted(p for p in dataset_dir.glob("*.json") if p.is_file())
    if limit is not None:
        paths = paths[:limit]
    if not paths:
        msg = f"No puzzle JSON files found in {dataset_dir}"
        raise ValueError(msg)

    puzzles: list[tuple[str, QueensPuzzle, str]] = []
    for path in paths:
        puzzle = parse_puzzle_file(path)
        puzzles.append((_puzzle_id_from_path(path), puzzle, "unknown"))
    return puzzles


def _load_puzzles_recursive(
    dataset_dir: Path,
    limit: int | None,
) -> dict[str, list[tuple[str, QueensPuzzle, str]]]:
    if dataset_dir.is_file():
        entries = load_manifest(dataset_dir)
        if limit is not None:
            entries = entries[:limit]
        grouped: dict[str, list[tuple[str, QueensPuzzle, str]]] = defaultdict(list)
        for entry in entries:
            payload = {
                "game": "queens",
                "n": entry["n"],
                "regions": entry["regions"],
                "givens": entry.get("givens", {"queens": [], "blocked": []}),
            }
            puzzle = parse_puzzle_dict(payload)
            size_key = f"size_{entry['n']}"
            puzzle_id = f"manifest_{entry['id']}"
            source = entry.get("source", "unknown")
            grouped[size_key].append((puzzle_id, puzzle, source))
        if not grouped:
            msg = f"No puzzles found in manifest: {dataset_dir}"
            raise ValueError(msg)
        return grouped

    if not dataset_dir.exists():
        msg = f"Dataset directory does not exist: {dataset_dir}"
        raise ValueError(msg)

    size_dirs = sorted(p for p in dataset_dir.glob("size_*") if p.is_dir())
    if not size_dirs:
        msg = f"No size_* directories found under {dataset_dir}"
        raise ValueError(msg)

    grouped: dict[str, list[tuple[str, QueensPuzzle, str]]] = {}
    for size_dir in size_dirs:
        size_key = size_dir.name
        grouped[size_key] = _load_puzzles(size_dir, limit=limit)
    return grouped


def _parse_dataset_paths(raw: str | Path) -> list[Path]:
    raw_str = str(raw)
    parts = [part.strip() for part in raw_str.split(",") if part.strip()]
    return [Path(part) for part in parts]


def run_benchmark(
    dataset_path: Path,
    algo_csv: str,
    limit: int | None = None,
    time_limit_s: float | None = None,
) -> list[BenchRow]:
    algo_names = _parse_algo_list(algo_csv)
    puzzles = _load_puzzles(dataset_path, limit=limit)

    rows: list[BenchRow] = []
    for puzzle_id, puzzle, source in puzzles:
        for algo in algo_names:
            solver = get_solver(algo)
            result = solver(puzzle, time_limit_s=time_limit_s)
            rows.append(
                BenchRow(
                    puzzle_id=puzzle_id,
                    algo=algo,
                    solved=result.solved,
                    metrics=result.metrics,
                    error=result.error,
                    n=puzzle.n,
                    source=source,
                )
            )
    return rows


def run_benchmark_multi(
    dataset_paths: Iterable[Path],
    algo_csv: str,
    limit: int | None = None,
    time_limit_s: float | None = None,
) -> list[BenchRow]:
    rows: list[BenchRow] = []
    for path in dataset_paths:
        rows.extend(run_benchmark(path, algo_csv, limit=limit, time_limit_s=time_limit_s))
    return rows


def _summarize(rows: list[BenchRow]) -> list[AlgoSummary]:
    grouped: dict[str, list[BenchRow]] = defaultdict(list)
    for row in rows:
        grouped[row.algo].append(row)

    summaries: list[AlgoSummary] = []
    for algo, algo_rows in grouped.items():
        puzzles = len(algo_rows)
        solved_rows = [row for row in algo_rows if row.solved]
        solved = len(solved_rows)
        solve_rate = 0.0 if puzzles == 0 else solved / puzzles

        time_values = [row.metrics.time_ms for row in solved_rows]
        node_values = [float(row.metrics.nodes) for row in solved_rows]
        backtrack_values = [float(row.metrics.backtracks) for row in solved_rows]

        summaries.append(
            AlgoSummary(
                algo=algo,
                puzzles=puzzles,
                solved=solved,
                solve_rate=solve_rate,
                avg_time_ms=mean(time_values) if time_values else 0.0,
                median_time_ms=_median(time_values),
                avg_nodes=mean(node_values) if node_values else 0.0,
                avg_backtracks=mean(backtrack_values) if backtrack_values else 0.0,
            )
        )

    summaries.sort(key=lambda item: (item.avg_time_ms, -item.solve_rate))
    return summaries


def _bar(value: float, max_value: float, width: int = 32) -> str:
    if max_value <= 0:
        return ""
    scaled = int((value / max_value) * width)
    return "#" * max(1, scaled)


def _chart_section(title: str, pairs: list[tuple[str, float]]) -> str:
    if not pairs:
        return f"### {title}\n\n_No data._"
    max_value = max(value for _, value in pairs)
    lines = [f"### {title}", "", "```text"]
    for name, value in pairs:
        bar = _bar(value, max_value)
        lines.append(f"{name:18} | {bar:32} | {value:10.3f}")
    lines.append("```")
    return "\n".join(lines)


def _summary_table(summaries: list[AlgoSummary]) -> str:
    header = (
        "| algo | puzzles | solved | solve_rate | avg_time_ms | median_time_ms | avg_nodes | avg_backtracks |"
    )
    divider = "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"
    rows = [header, divider]
    for item in summaries:
        rows.append(
            f"| {item.algo} | {item.puzzles} | {item.solved} | {item.solve_rate:.2%} | "
            f"{item.avg_time_ms:.3f} | {item.median_time_ms:.3f} | {item.avg_nodes:.1f} | "
            f"{item.avg_backtracks:.1f} |"
        )
    return "\n".join(rows)


def _top_k_by_time(rows: list[BenchRow], k: int) -> dict[str, list[BenchRow]]:
    grouped: dict[str, list[BenchRow]] = defaultdict(list)
    for row in rows:
        if row.solved:
            grouped[row.algo].append(row)

    top: dict[str, list[BenchRow]] = {}
    for algo, algo_rows in grouped.items():
        ordered = sorted(algo_rows, key=lambda item: item.metrics.time_ms, reverse=True)
        top[algo] = ordered[:k]
    return top


def _top_k_section(rows: list[BenchRow], k: int) -> str:
    if k <= 0:
        return ""
    top = _top_k_by_time(rows, k)
    lines = ["### Slowest Puzzles (by time)", "", "```text"]
    for algo, algo_rows in top.items():
        lines.append(f"{algo}:")
        if not algo_rows:
            lines.append("  (no solved puzzles)")
            continue
        for row in algo_rows:
            lines.append(
                f"  {row.puzzle_id:20} | {row.metrics.time_ms:10.3f} ms | nodes={row.metrics.nodes}"
            )
    lines.append("```")
    return "\n".join(lines)


def _timeouts_section(rows: list[BenchRow]) -> str:
    timeouts: dict[str, int] = defaultdict(int)
    totals: dict[str, int] = defaultdict(int)

    for row in rows:
        totals[row.algo] += 1
        if row.error and "timeout" in row.error.lower():
            timeouts[row.algo] += 1

    if not totals:
        return ""

    lines = ["### Timeouts by Algorithm", "", "```text"]
    for algo in sorted(totals):
        count = timeouts.get(algo, 0)
        total = totals[algo]
        rate = 0.0 if total == 0 else (count / total) * 100.0
        lines.append(f"{algo:18} | {count:3d} / {total:3d} | {rate:6.2f}%")
    lines.append("```")
    return "\n".join(lines)


def build_report(
    rows: list[BenchRow],
    dataset_label: str,
    top_k: int = 3,
    time_limit_s: float | None = None,
) -> str:
    summaries = _summarize(rows)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    avg_time_pairs = [(item.algo, item.avg_time_ms) for item in summaries]
    avg_node_pairs = [(item.algo, item.avg_nodes) for item in summaries]

    sections = [
        "# Queens Benchmark Report",
        "",
        f"- Generated: {now}",
        f"- Dataset: `{dataset_label}`",
        f"- Algorithms: {', '.join(item.algo for item in summaries)}",
        f"- Time limit: {time_limit_s}s" if time_limit_s is not None else "- Time limit: none",
        "",
        "## Summary",
        "",
        _summary_table(summaries),
        "",
        "## Charts",
        "",
        _chart_section("Average Time (ms)", avg_time_pairs),
        "",
        _chart_section("Average Nodes", avg_node_pairs),
    ]

    top_section = _top_k_section(rows, top_k)
    if top_section:
        sections.extend(["", "## Slowest Puzzles", "", top_section])

    timeouts_section = _timeouts_section(rows)
    if timeouts_section:
        sections.extend(["", "## Timeouts", "", timeouts_section])

    sections.extend(
        [
            "",
            "## Notes",
            "",
            "- Times are measured inside each solver using `perf_counter()`.",
            "- Averages and medians are computed over solved puzzles only.",
            "- This report is ASCII-only to stay portable in terminals and GitHub Markdown.",
        ]
    )
    return "\n".join(sections)


def _section_title(name: str) -> str:
    return f"## {name.replace('_', ' ').title()}"


def build_report_recursive(
    grouped_rows: dict[str, list[BenchRow]],
    dataset_label: str,
    top_k: int = 3,
    time_limit_s: float | None = None,
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_rows = [row for rows in grouped_rows.values() for row in rows]
    all_algos = sorted({row.algo for row in all_rows})

    sections = [
        "# Queens Benchmark Report (Recursive)",
        "",
        f"- Generated: {now}",
        f"- Dataset root: `{dataset_label}`",
        f"- Algorithms: {', '.join(all_algos)}",
        f"- Time limit: {time_limit_s}s" if time_limit_s is not None else "- Time limit: none",
        "",
        "## Global Summary",
        "",
        _summary_table(_summarize(all_rows)),
    ]

    for size_key in sorted(grouped_rows):
        size_rows = grouped_rows[size_key]
        summaries = _summarize(size_rows)
        sections.extend(
            [
                "",
                _section_title(size_key),
                "",
                _summary_table(summaries),
            ]
        )

        avg_time_pairs = [(item.algo, item.avg_time_ms) for item in summaries]
        avg_node_pairs = [(item.algo, item.avg_nodes) for item in summaries]
        sections.extend(
            [
                "",
                _chart_section("Average Time (ms)", avg_time_pairs),
                "",
                _chart_section("Average Nodes", avg_node_pairs),
                "",
                _top_k_section(size_rows, top_k),
                "",
                _timeouts_section(size_rows),
            ]
        )

    sections.extend(
        [
            "",
            "## Notes",
            "",
            "- Times are measured inside each solver using `perf_counter()`.",
            "- Averages and medians are computed over solved puzzles only.",
            "- This report is ASCII-only to stay portable in terminals and GitHub Markdown.",
        ]
    )
    return "\n".join(sections)


def _write_runs_jsonl(rows: list[BenchRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for idx, row in enumerate(rows, start=1):
            record = {
                "id": idx,
                "puzzle_id": row.puzzle_id,
                "n": row.n,
                "algo": row.algo,
                "solved": row.solved,
                "time_ms": row.metrics.time_ms,
                "nodes": row.metrics.nodes,
                "backtracks": row.metrics.backtracks,
                "timeout": bool(row.error and "timeout" in row.error.lower()),
                "source": row.source,
            }
            handle.write(json.dumps(record, separators=(",", ":")) + "\n")


def run_and_report(
    dataset: str | Path,
    algo_csv: str,
    report_path: Path,
    limit: int | None = None,
    recursive: bool = False,
    top_k: int = 3,
    time_limit_s: float | None = None,
    runs_out: Path | None = None,
) -> tuple[list[BenchRow], str]:
    dataset_paths = _parse_dataset_paths(dataset)

    if recursive:
        grouped_rows: dict[str, list[BenchRow]] = defaultdict(list)
        for path in dataset_paths:
            grouped_puzzles = _load_puzzles_recursive(path, limit=limit)
            for size_key, puzzles in grouped_puzzles.items():
                rows: list[BenchRow] = []
                algo_names = _parse_algo_list(algo_csv)
                for puzzle_id, puzzle, source in puzzles:
                    for algo in algo_names:
                        solver = get_solver(algo)
                        result = solver(puzzle, time_limit_s=time_limit_s)
                        rows.append(
                            BenchRow(
                                puzzle_id=f"{size_key}/{puzzle_id}",
                                algo=algo,
                                solved=result.solved,
                                metrics=result.metrics,
                                error=result.error,
                                n=puzzle.n,
                                source=source,
                            )
                        )
                grouped_rows[size_key].extend(rows)
        report = build_report_recursive(grouped_rows, dataset_label=dataset, top_k=top_k, time_limit_s=time_limit_s)
        all_rows = [row for rows in grouped_rows.values() for row in rows]
    else:
        all_rows = run_benchmark_multi(
            dataset_paths,
            algo_csv,
            limit=limit,
            time_limit_s=time_limit_s,
        )
        report = build_report(all_rows, dataset_label=dataset, top_k=top_k, time_limit_s=time_limit_s)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    if runs_out is not None:
        _write_runs_jsonl(all_rows, runs_out)

    return all_rows, report


def available_algorithms() -> list[str]:
    return list_solvers()
