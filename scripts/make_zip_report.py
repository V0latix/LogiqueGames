#!/usr/bin/env python3
"""Generate a Zip data science report with charts."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_fig(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def load_runs(path: Path) -> pd.DataFrame:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    df = pd.DataFrame(rows)
    if "puzzle_id" in df.columns:
        df["puzzle_id"] = pd.to_numeric(df["puzzle_id"], errors="coerce")
    return df


def load_manifest(path: Path) -> pd.DataFrame:
    data = json.loads(path.read_text(encoding="utf-8"))
    puzzles = data.get("puzzles", [])
    df = pd.DataFrame(puzzles)
    if not df.empty:
        df["puzzle_id"] = pd.to_numeric(df["id"], errors="coerce")
        df["checkpoint_count"] = df["numbers"].apply(lambda x: len(x) if isinstance(x, list) else 0)
        df["wall_count"] = df["walls"].apply(lambda x: len(x) if isinstance(x, list) else 0)
        df["edge_count"] = df["n"].apply(lambda n: int(n * (n - 1) * 2))
        df["wall_density"] = df.apply(
            lambda row: (row["wall_count"] / row["edge_count"]) if row["edge_count"] else 0.0, axis=1
        )
    return df


def percentile(values: pd.Series, q: float) -> float:
    if values.empty:
        return 0.0
    return float(values.quantile(q))


def aggregate_global(df_runs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for algo, group in df_runs.groupby("algo"):
        solved = group[group["solved"]]
        rows.append(
            {
                "algo": algo,
                "puzzles": len(group),
                "solved": int(group["solved"].sum()),
                "solved_rate": group["solved"].mean() if len(group) else 0.0,
                "timeout_rate": group["timeout"].mean() if "timeout" in group else 0.0,
                "median_time_ms_solved": percentile(solved["time_ms"], 0.5),
                "p90_time_ms_solved": percentile(solved["time_ms"], 0.9),
                "p99_time_ms_solved": percentile(solved["time_ms"], 0.99),
                "median_nodes_solved": percentile(solved["nodes"], 0.5),
                "median_backtracks_solved": percentile(solved["backtracks"], 0.5),
            }
        )
    return pd.DataFrame(rows).sort_values("algo")


def aggregate_by_source(df_runs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (algo, source), group in df_runs.groupby(["algo", "source"], dropna=False):
        solved = group[group["solved"]]
        rows.append(
            {
                "algo": algo,
                "source": source,
                "puzzles": len(group),
                "solved": int(group["solved"].sum()),
                "solved_rate": group["solved"].mean() if len(group) else 0.0,
                "timeout_rate": group["timeout"].mean() if "timeout" in group else 0.0,
                "median_time_ms_solved": percentile(solved["time_ms"], 0.5),
            }
        )
    return pd.DataFrame(rows).sort_values(["algo", "source"])


def aggregate_by_size(df_runs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (n, algo), group in df_runs.groupby(["n", "algo"], dropna=False):
        solved = group[group["solved"]]
        rows.append(
            {
                "n": int(n),
                "algo": algo,
                "puzzles": len(group),
                "solved_rate": group["solved"].mean() if len(group) else 0.0,
                "timeout_rate": group["timeout"].mean() if "timeout" in group else 0.0,
                "median_time_ms_solved": percentile(solved["time_ms"], 0.5),
                "p90_time_ms_solved": percentile(solved["time_ms"], 0.9),
                "p99_time_ms_solved": percentile(solved["time_ms"], 0.99),
                "median_nodes_solved": percentile(solved["nodes"], 0.5),
            }
        )
    return pd.DataFrame(rows).sort_values(["n", "algo"])


def size_distribution(df_puzzles: pd.DataFrame) -> pd.DataFrame:
    return df_puzzles.groupby(["n", "source"], as_index=False)["puzzle_id"].count().rename(
        columns={"puzzle_id": "puzzles"}
    )


def relative_vs_baseline(df_runs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    baseline = df_runs[df_runs["algo"] == "baseline"]
    for algo in sorted(df_runs["algo"].unique()):
        if algo == "baseline":
            continue
        other = df_runs[df_runs["algo"] == algo]
        merged = baseline.merge(
            other,
            on=["puzzle_id"],
            suffixes=("_base", "_algo"),
        )
        solved = merged[(merged["solved_base"]) & (merged["solved_algo"])]
        speedup = None
        if not solved.empty:
            speedup = (solved["time_ms_algo"] / solved["time_ms_base"]).median()
        rows.append(
            {
                "algo": algo,
                "speedup_median": speedup if speedup is not None else 0.0,
                "delta_solve_rate": other["solved"].mean() - baseline["solved"].mean(),
            }
        )
    return pd.DataFrame(rows).sort_values("algo")


def hardest_puzzles(df_runs: pd.DataFrame, top_k: int = 5) -> pd.DataFrame:
    rows = []
    for algo, group in df_runs.groupby("algo"):
        solved = group[group["solved"]].sort_values("time_ms", ascending=False).head(top_k)
        for _, row in solved.iterrows():
            rows.append(
                {
                    "algo": algo,
                    "puzzle_id": int(row["puzzle_id"]),
                    "source": row.get("source", "unknown"),
                    "n": int(row["n"]),
                    "time_ms": float(row["time_ms"]),
                    "nodes": int(row["nodes"]),
                    "backtracks": int(row["backtracks"]),
                }
            )
    return pd.DataFrame(rows)


def plot_size_distribution(df_sizes: pd.DataFrame, out: Path) -> None:
    data = df_sizes.pivot(index="n", columns="source", values="puzzles").fillna(0)
    data.plot(kind="bar", stacked=True, figsize=(10, 4))
    plt.title("Puzzle Count by Size (n) and Source")
    plt.xlabel("n")
    plt.ylabel("puzzles")
    save_fig(out)


def plot_median_time_by_size(df: pd.DataFrame, out: Path) -> None:
    data = df.copy()
    if data.empty:
        return
    sns.lineplot(data=data, x="n", y="median_time_ms_solved", hue="algo", marker="o")
    plt.title("Median Solve Time by Size (Solved Only)")
    save_fig(out)


def plot_solve_rate(df_runs: pd.DataFrame, out: Path) -> None:
    data = df_runs.groupby("algo", as_index=False)["solved"].mean()
    sns.barplot(data=data, x="algo", y="solved")
    plt.title("Solve Rate by Algorithm")
    plt.ylabel("solve_rate")
    plt.xticks(rotation=30, ha="right")
    save_fig(out)


def plot_time_box(df_runs: pd.DataFrame, out: Path) -> None:
    data = df_runs[df_runs["solved"]]
    if data.empty:
        return
    sns.boxplot(data=data, x="algo", y="time_ms")
    plt.title("Solve Time Distribution (ms) — solved only")
    plt.xticks(rotation=30, ha="right")
    save_fig(out)


def write_report(
    runs_path: Path,
    manifest_path: Path,
    output_path: Path,
    figdir: Path,
) -> None:
    df_runs = load_runs(runs_path)
    df_puzzles = load_manifest(manifest_path)
    if "source" not in df_runs.columns:
        df_runs["source"] = "unknown"
    if not df_puzzles.empty:
        df_runs = df_runs.merge(
            df_puzzles[["puzzle_id", "source", "checkpoint_count", "wall_count", "wall_density"]],
            on="puzzle_id",
            how="left",
            suffixes=("", "_manifest"),
        )
        if "source_manifest" in df_runs.columns:
            df_runs["source"] = df_runs["source"].fillna(df_runs["source_manifest"])
            df_runs = df_runs.drop(columns=["source_manifest"])

    overview = {
        "runs": len(df_runs),
        "unique_puzzles": df_puzzles["puzzle_id"].nunique() if not df_puzzles.empty else 0,
        "sources": df_puzzles["source"].value_counts().to_dict() if not df_puzzles.empty else {},
    }

    size_dist = size_distribution(df_puzzles) if not df_puzzles.empty else pd.DataFrame()
    summary = aggregate_global(df_runs)
    by_source = aggregate_by_source(df_runs)
    by_size = aggregate_by_size(df_runs)
    rel = relative_vs_baseline(df_runs)
    hard = hardest_puzzles(df_runs, top_k=5)

    ensure_dir(figdir)
    if not size_dist.empty:
        plot_size_distribution(size_dist, figdir / "zip_size_distribution.png")
    plot_median_time_by_size(by_size, figdir / "zip_median_time_by_size.png")
    plot_solve_rate(df_runs, figdir / "zip_solve_rate.png")
    plot_time_box(df_runs, figdir / "zip_time_box.png")

    md = [
        "# Zip Data Science Report",
        "",
        "## Dataset Overview",
        f"- Runs: {overview['runs']}",
        f"- Unique puzzles: {overview['unique_puzzles']}",
        f"- Source distribution: {overview['sources']}",
        "",
    ]

    if not size_dist.empty:
        md.extend(
            [
                "### Size Distribution",
                "",
                size_dist.to_markdown(index=False),
                "",
                f"![Size Distribution](figures/zip_size_distribution.png)",
                "",
            ]
        )

    md.extend(
        [
            "## Global Performance Summary",
            "",
            summary.to_markdown(index=False),
            "",
            "## Performance by Source",
            "",
            by_source.to_markdown(index=False),
            "",
            "## Performance by Size",
            "",
            by_size.to_markdown(index=False),
            "",
            f"![Median Time by Size](figures/zip_median_time_by_size.png)",
            "",
            f"![Solve Rate](figures/zip_solve_rate.png)",
            "",
            f"![Time Distribution](figures/zip_time_box.png)",
            "",
            "## Relative Performance vs Baseline",
            "",
            rel.to_markdown(index=False),
            "",
            "## Hardest Puzzles (Top 5 per Algo)",
            "",
            hard.to_markdown(index=False),
        ]
    )

    output_path.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Zip report")
    parser.add_argument("--runs", type=Path, default=Path("data/benchmarks/zip_runs.jsonl"))
    parser.add_argument("--manifest", type=Path, default=Path("data/zip_unique.json"))
    parser.add_argument("--out", type=Path, default=Path("reports/zip_report.md"))
    parser.add_argument("--figdir", type=Path, default=Path("reports/figures"))
    args = parser.parse_args()

    write_report(args.runs, args.manifest, args.out, args.figdir)
    print(f"Wrote report to {args.out}")


if __name__ == "__main__":
    main()
