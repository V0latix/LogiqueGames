#!/usr/bin/env python3
"""Fill missing benchmark runs for puzzles/algorithms.

This script appends only missing (puzzle_id, algo) pairs to a runs JSONL file.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from linkedin_game_solver.datasets.exporter import load_manifest
from linkedin_game_solver.games.queens.parser import parse_puzzle_dict
from linkedin_game_solver.games.queens.solvers import get_solver, list_solvers


def _parse_algo_list(raw: str | None) -> list[str]:
    if raw is None:
        return list_solvers()
    parts = [part.strip() for part in raw.split(",") if part.strip()]
    if not parts:
        msg = "No algorithms provided."
        raise ValueError(msg)
    for name in parts:
        get_solver(name)
    return parts


def _load_puzzles(manifest_path: Path, limit: int | None) -> list[tuple[str, dict, str]]:
    entries = load_manifest(manifest_path)
    if limit is not None:
        entries = entries[:limit]
    puzzles: list[tuple[str, dict, str]] = []
    for entry in entries:
        payload = {
            "game": "queens",
            "n": entry["n"],
            "regions": entry["regions"],
            "givens": entry.get("givens", {"queens": [], "blocked": []}),
        }
        # Validate payload early
        parse_puzzle_dict(payload)
        puzzle_id = f"manifest_{entry['id']}"
        source = entry.get("source", "unknown")
        puzzles.append((puzzle_id, payload, source))
    if not puzzles:
        msg = f"No puzzles found in manifest: {manifest_path}"
        raise ValueError(msg)
    return puzzles


def _parse_manifest_list(raw: str) -> list[Path]:
    parts = [part.strip() for part in raw.split(",") if part.strip()]
    if not parts:
        msg = "No manifests provided."
        raise ValueError(msg)
    return [Path(part) for part in parts]


def _load_existing_runs(runs_path: Path) -> tuple[set[tuple[str, str]], int]:
    existing: set[tuple[str, str]] = set()
    max_id = 0
    if not runs_path.exists():
        return existing, max_id

    with runs_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            puzzle_id = str(record.get("puzzle_id", ""))
            algo = str(record.get("algo", ""))
            if puzzle_id and algo:
                existing.add((puzzle_id, algo))
            max_id = max(max_id, int(record.get("id", 0)))
    return existing, max_id


def _append_runs(
    runs_path: Path,
    puzzles: list[tuple[str, dict, str]],
    algos: list[str],
    time_limit_s: float | None,
    start_id: int,
) -> int:
    runs_path.parent.mkdir(parents=True, exist_ok=True)
    next_id = start_id
    appended = 0

    with runs_path.open("a", encoding="utf-8") as handle:
        for puzzle_id, payload, source in puzzles:
            puzzle = parse_puzzle_dict(payload)
            for algo in algos:
                solver = get_solver(algo)
                result = solver(puzzle, time_limit_s=time_limit_s)
                next_id += 1
                record = {
                    "id": next_id,
                    "puzzle_id": puzzle_id,
                    "n": puzzle.n,
                    "algo": algo,
                    "solved": result.solved,
                    "time_ms": result.metrics.time_ms,
                    "nodes": result.metrics.nodes,
                    "backtracks": result.metrics.backtracks,
                    "timeout": bool(result.error and "timeout" in result.error.lower()),
                    "source": source,
                }
                handle.write(json.dumps(record, separators=(",", ":")) + "\n")
                appended += 1
    return appended


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append missing benchmark runs for a puzzles manifest.",
    )
    parser.add_argument(
        "--manifest",
        required=True,
        help="Comma-separated manifest paths (e.g., data/puzzles.json,data/puzzles_generated.json).",
    )
    parser.add_argument(
        "--runs",
        type=Path,
        default=Path("data/benchmarks/queens_runs.jsonl"),
        help="Runs JSONL file to update (default: data/benchmarks/queens_runs.jsonl).",
    )
    parser.add_argument(
        "--algos",
        default=None,
        help="Comma-separated list of algorithms (default: all).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on puzzles to consider (first N).",
    )
    parser.add_argument(
        "--timelimit",
        type=float,
        default=1.0,
        help="Time limit per puzzle in seconds (default: 1.0).",
    )
    args = parser.parse_args()

    algos = _parse_algo_list(args.algos)
    manifests = _parse_manifest_list(args.manifest)
    puzzles: list[tuple[str, dict, str]] = []
    for manifest in manifests:
        puzzles.extend(_load_puzzles(manifest, args.limit))
    existing, max_id = _load_existing_runs(args.runs)

    missing_pairs = 0
    appended = 0
    for puzzle_id, payload, source in puzzles:
        for algo in algos:
            if (puzzle_id, algo) in existing:
                continue
            missing_pairs += 1
            appended += _append_runs(args.runs, [(puzzle_id, payload, source)], [algo], args.timelimit, max_id)
            max_id += 1
            existing.add((puzzle_id, algo))

    if appended == 0:
        print("No missing runs. Nothing to do.")
        return 0

    print(f"Missing pairs: {missing_pairs}")
    print(f"Appended runs: {appended}")
    print(f"Updated file: {args.runs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
