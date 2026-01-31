"""Utilities for building the Queens data science report."""

from __future__ import annotations

import json
import math
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def load_runs(path: Path, drop_algos: set[str] | None = None) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    if not records:
        raise ValueError(f"No records found in {path}")
    df = pd.DataFrame.from_records(records)
    if "source" not in df.columns:
        df["source"] = "unknown"
    if "algo" not in df.columns:
        raise ValueError("runs JSONL must include an 'algo' field")
    if drop_algos:
        df = df[~df["algo"].isin(drop_algos)].reset_index(drop=True)
    df["puzzle_id"] = df["puzzle_id"].apply(_coerce_puzzle_id)
    return df


def load_manifest(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("game") != "queens" or "puzzles" not in payload:
        msg = f"Invalid manifest: {path}"
        raise ValueError(msg)
    return payload


def _coerce_puzzle_id(value: Any) -> int:
    if isinstance(value, int):
        return value
    text = str(value)
    if text.startswith("manifest_"):
        text = text.split("manifest_", 1)[1]
    return int(text)


def percentile(series: pd.Series, q: float) -> float:
    values = series.dropna().to_numpy()
    if values.size == 0:
        return float("nan")
    return float(np.percentile(values, q))


def gini(values: list[int] | np.ndarray) -> float:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return float("nan")
    if np.all(arr == 0):
        return 0.0
    arr = np.sort(arr)
    n = arr.size
    cum = np.cumsum(arr)
    return float((n + 1 - 2 * np.sum(cum) / cum[-1]) / n)


def coeff_variation(values: list[int] | np.ndarray) -> float:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return float("nan")
    mean = float(np.mean(arr))
    if mean == 0:
        return float("nan")
    return float(np.std(arr, ddof=0) / mean)


def puzzle_features(regions: list[list[int]]) -> dict[str, float]:
    n = len(regions)
    region_ids = {cell for row in regions for cell in row}
    region_sizes: dict[int, int] = {rid: 0 for rid in region_ids}
    region_rows: dict[int, set[int]] = {rid: set() for rid in region_ids}
    region_cols: dict[int, set[int]] = {rid: set() for rid in region_ids}
    boundary_edges = 0

    for r, row in enumerate(regions):
        for c, rid in enumerate(row):
            region_sizes[rid] += 1
            region_rows[rid].add(r)
            region_cols[rid].add(c)
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if nr < 0 or nr >= n or nc < 0 or nc >= n:
                    boundary_edges += 1
                elif regions[nr][nc] != rid:
                    boundary_edges += 1

    sizes = list(region_sizes.values())
    row_spreads = [len(rows) for rows in region_rows.values()]
    col_spreads = [len(cols) for cols in region_cols.values()]

    singleton = sum(1 for size in sizes if size == 1)
    small = sum(1 for size in sizes if size <= 3)
    large = sum(1 for size in sizes if size >= n)

    return {
        "n": float(n),
        "num_regions": float(len(region_ids)),
        "region_size_min": float(np.min(sizes)),
        "region_size_mean": float(np.mean(sizes)),
        "region_size_median": float(np.median(sizes)),
        "region_size_max": float(np.max(sizes)),
        "region_size_std": float(np.std(sizes, ddof=0)),
        "region_size_cv": coeff_variation(sizes),
        "region_size_gini": gini(sizes),
        "singleton_regions": float(singleton),
        "small_regions_le_3": float(small),
        "large_regions_ge_n": float(large),
        "row_spread_mean": float(np.mean(row_spreads)),
        "row_spread_max": float(np.max(row_spreads)),
        "col_spread_mean": float(np.mean(col_spreads)),
        "col_spread_max": float(np.max(col_spreads)),
        "boundary_edges": float(boundary_edges),
        "boundary_edges_per_cell": float(boundary_edges) / (n * n),
    }


def build_features_df(manifest: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for puzzle in manifest["puzzles"]:
        row = puzzle_features(puzzle["regions"])
        row["puzzle_id"] = int(puzzle["id"])
        row["source"] = puzzle.get("source", "unknown")
        row["solution"] = puzzle.get("solution", "unknown")
        rows.append(row)
    return pd.DataFrame(rows)


def dataset_overview(df_runs: pd.DataFrame, df_features: pd.DataFrame) -> dict[str, Any]:
    overview = {
        "runs": int(len(df_runs)),
        "unique_puzzles": int(df_runs["puzzle_id"].nunique()),
        "sources": df_runs["source"].value_counts(dropna=False).to_dict(),
    }
    if "solution" in df_features.columns:
        overview["solution_status"] = df_features["solution"].value_counts(dropna=False).to_dict()
    return overview


def size_distribution(df_features: pd.DataFrame) -> pd.DataFrame:
    grouped = df_features.groupby(["n", "source"], as_index=False)["puzzle_id"].count()
    grouped = grouped.rename(columns={"puzzle_id": "puzzles"})
    return grouped.sort_values(["n", "source"])


def aggregate_global(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("algo", as_index=False)
    summary = grouped.agg(
        runs=("algo", "count"),
        puzzles=("puzzle_id", "nunique"),
        solved=("solved", "sum"),
        solved_rate=("solved", "mean"),
        timeout_rate=("timeout", "mean"),
        avg_time_ms=("time_ms", lambda s: s[df.loc[s.index, "solved"]].mean()),
        median_time_ms=("time_ms", lambda s: s[df.loc[s.index, "solved"]].median()),
        p90_time_ms=("time_ms", lambda s: percentile(s[df.loc[s.index, "solved"]], 90)),
        p99_time_ms=("time_ms", lambda s: percentile(s[df.loc[s.index, "solved"]], 99)),
        median_nodes=("nodes", lambda s: s[df.loc[s.index, "solved"]].median()),
        p90_nodes=("nodes", lambda s: percentile(s[df.loc[s.index, "solved"]], 90)),
        avg_backtracks=("backtracks", lambda s: s[df.loc[s.index, "solved"]].mean()),
    )
    return summary.sort_values(by=["median_time_ms", "solved_rate"], ascending=[True, False])


def aggregate_by_source(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(["source", "algo"], as_index=False)
    summary = grouped.agg(
        runs=("algo", "count"),
        puzzles=("puzzle_id", "nunique"),
        solved=("solved", "sum"),
        solved_rate=("solved", "mean"),
        timeout_rate=("timeout", "mean"),
        median_time_ms=("time_ms", lambda s: s[df.loc[s.index, "solved"]].median()),
        p90_time_ms=("time_ms", lambda s: percentile(s[df.loc[s.index, "solved"]], 90)),
        median_nodes=("nodes", lambda s: s[df.loc[s.index, "solved"]].median()),
    )
    return summary.sort_values(by=["source", "median_time_ms"], ascending=[True, True])


def aggregate_by_size(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(["n", "algo"], as_index=False)
    summary = grouped.agg(
        runs=("algo", "count"),
        puzzles=("puzzle_id", "nunique"),
        solved=("solved", "sum"),
        solved_rate=("solved", "mean"),
        timeout_rate=("timeout", "mean"),
        median_time_ms_solved=("time_ms", lambda s: s[df.loc[s.index, "solved"]].median()),
        p90_time_ms_solved=("time_ms", lambda s: percentile(s[df.loc[s.index, "solved"]], 90)),
        p99_time_ms_solved=("time_ms", lambda s: percentile(s[df.loc[s.index, "solved"]], 99)),
        median_time_ms_all=("time_ms", "median"),
        p90_time_ms_all=("time_ms", lambda s: percentile(s, 90)),
        p99_time_ms_all=("time_ms", lambda s: percentile(s, 99)),
        median_nodes=("nodes", lambda s: s[df.loc[s.index, "solved"]].median()),
        p90_nodes=("nodes", lambda s: percentile(s[df.loc[s.index, "solved"]], 90)),
    )
    return summary.sort_values(by=["n", "median_time_ms_solved"], ascending=[True, True])


def relative_vs_dlx(df: pd.DataFrame) -> pd.DataFrame:
    if "dlx" not in set(df["algo"]):
        return pd.DataFrame()
    dlx = df[df["algo"] == "dlx"][["puzzle_id", "time_ms", "solved"]]
    dlx = dlx.rename(columns={"time_ms": "dlx_time_ms", "solved": "dlx_solved"})
    rows: list[dict[str, Any]] = []
    for algo in sorted(set(df["algo"]) - {"dlx"}):
        subset = df[df["algo"] == algo].merge(dlx, on="puzzle_id", how="inner")
        both_solved = subset[subset["solved"] & subset["dlx_solved"]]
        if both_solved.empty:
            continue
        ratio = both_solved["time_ms"] / both_solved["dlx_time_ms"]
        rows.append(
            {
                "algo": algo,
                "speedup_median": float(np.median(ratio)),
                "speedup_p90": float(np.percentile(ratio, 90)),
                "speedup_p99": float(np.percentile(ratio, 99)),
                "delta_solve_rate": float(df[df["algo"] == algo]["solved"].mean() - 1.0),
            }
        )
    return pd.DataFrame(rows).sort_values(by=["speedup_median"])


def ablation_backtracking(df: pd.DataFrame) -> pd.DataFrame:
    needed = {"backtracking_bb", "backtracking_bb_nolcv"}
    if not needed.issubset(set(df["algo"])):
        return pd.DataFrame()
    base = df[df["algo"] == "backtracking_bb"][["puzzle_id", "time_ms", "nodes", "backtracks", "timeout", "solved"]]
    ablation = df[df["algo"] == "backtracking_bb_nolcv"][
        ["puzzle_id", "time_ms", "nodes", "backtracks", "timeout", "solved"]
    ]
    merged = base.merge(ablation, on="puzzle_id", suffixes=("_lcv", "_nolcv"))
    solved = merged[merged["solved_lcv"] & merged["solved_nolcv"]]
    if solved.empty:
        return pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "metric": "time_ms",
                "median_ratio": float(np.median(solved["time_ms_nolcv"] / solved["time_ms_lcv"])),
                "p90_ratio": float(np.percentile(solved["time_ms_nolcv"] / solved["time_ms_lcv"], 90)),
            },
            {
                "metric": "nodes",
                "median_ratio": float(np.median(solved["nodes_nolcv"] / solved["nodes_lcv"])),
                "p90_ratio": float(np.percentile(solved["nodes_nolcv"] / solved["nodes_lcv"], 90)),
            },
            {
                "metric": "backtracks",
                "median_ratio": float(np.median(solved["backtracks_nolcv"] / solved["backtracks_lcv"])),
                "p90_ratio": float(np.percentile(solved["backtracks_nolcv"] / solved["backtracks_lcv"], 90)),
            },
            {
                "metric": "timeout_rate",
                "median_ratio": float(merged["timeout_nolcv"].mean() / max(1e-9, merged["timeout_lcv"].mean())),
                "p90_ratio": float("nan"),
            },
        ]
    )


def correlate_features(
    df_features: pd.DataFrame,
    df_runs: pd.DataFrame,
    algo: str,
    metric: str,
) -> pd.DataFrame:
    runs = df_runs[df_runs["algo"] == algo]
    if runs.empty:
        return pd.DataFrame()
    keep_cols = ["puzzle_id", metric]
    keep_cols = [col for col in keep_cols if col in runs.columns]
    merged = df_features.merge(runs[keep_cols], on="puzzle_id", how="inner")
    if metric not in merged.columns:
        return pd.DataFrame()
    feature_cols = [col for col in df_features.columns if col not in {"puzzle_id", "source", "solution"}]
    rows: list[dict[str, Any]] = []
    for col in feature_cols:
        series = merged[col]
        if series.nunique() <= 1:
            continue
        corr = spearman_corr(series.to_numpy(), merged[metric].to_numpy())
        rows.append({"feature": col, "spearman_corr": float(corr), "abs_spearman": float(abs(corr))})
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values(by=["abs_spearman"], ascending=False)


def spearman_corr(x: np.ndarray, y: np.ndarray) -> float:
    if x.size == 0 or y.size == 0:
        return float("nan")
    x_rank = pd.Series(x).rank().to_numpy()
    y_rank = pd.Series(y).rank().to_numpy()
    if np.std(x_rank) == 0 or np.std(y_rank) == 0:
        return float("nan")
    return float(np.corrcoef(x_rank, y_rank)[0, 1])


def hardest_puzzles(df_runs: pd.DataFrame, algo: str, top_k: int) -> pd.DataFrame:
    subset = df_runs[df_runs["algo"] == algo].copy()
    if subset.empty:
        return pd.DataFrame()
    subset = subset.sort_values(
        by=["time_ms", "puzzle_id"],
        ascending=[False, True],
    ).head(top_k)
    return subset[
        ["puzzle_id", "source", "n", "time_ms", "nodes", "backtracks", "solved", "timeout"]
    ].reset_index(drop=True)


def features_profile(
    df_features: pd.DataFrame,
    df_runs: pd.DataFrame,
    algo: str,
    top_k: int,
) -> pd.DataFrame:
    subset = df_runs[df_runs["algo"] == algo].copy()
    if subset.empty:
        return pd.DataFrame()
    subset = subset.sort_values(
        by=["time_ms", "puzzle_id"],
        ascending=[False, True],
    ).head(top_k)
    merged = df_features.merge(subset[["puzzle_id"]], on="puzzle_id", how="inner")
    feature_cols = [col for col in df_features.columns if col not in {"puzzle_id", "source", "solution"}]
    return merged[feature_cols].mean().to_frame(name="mean").reset_index().rename(columns={"index": "feature"})


def bias_check(df_features: pd.DataFrame) -> pd.DataFrame:
    feature_cols = [col for col in df_features.columns if col not in {"puzzle_id", "source", "solution"}]
    grouped = df_features.groupby("source")[feature_cols].mean().reset_index()
    return grouped


def system_metadata() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "processor": platform.processor() or "unknown",
    }
