#!/usr/bin/env python3
"""Generate an actionable Queens data science report with charts."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from linkedin_game_solver.benchmarks.report_utils import (
    ablation_backtracking,
    aggregate_by_size,
    aggregate_by_source,
    aggregate_global,
    bias_check,
    build_features_df,
    correlate_features,
    dataset_overview,
    features_profile,
    hardest_puzzles,
    load_manifest,
    load_runs,
    relative_vs_dlx,
    size_distribution,
    system_metadata,
)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_fig(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


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


def plot_solve_rate_by_size(df: pd.DataFrame, out: Path) -> None:
    data = df.copy()
    if data.empty:
        return
    sns.lineplot(data=data, x="n", y="solved_rate", hue="algo", marker="o")
    plt.title("Solve Rate by Size")
    plt.ylabel("solve_rate")
    save_fig(out)


def plot_avg_time(df: pd.DataFrame, out: Path) -> None:
    data = df[df["solved"]].groupby("algo", as_index=False)["time_ms"].mean()
    sns.barplot(data=data, x="algo", y="time_ms")
    plt.title("Average Solve Time (ms) — solved only")
    plt.xticks(rotation=30, ha="right")
    save_fig(out)


def plot_solve_rate(df: pd.DataFrame, out: Path) -> None:
    data = df.groupby("algo", as_index=False)["solved"].mean()
    sns.barplot(data=data, x="algo", y="solved")
    plt.title("Solve Rate by Algorithm")
    plt.ylabel("solve_rate")
    plt.xticks(rotation=30, ha="right")
    save_fig(out)


def plot_time_box(df: pd.DataFrame, out: Path) -> None:
    data = df[df["solved"]]
    if data.empty:
        return
    sns.boxplot(data=data, x="algo", y="time_ms")
    plt.title("Solve Time Distribution (ms) — solved only")
    plt.xticks(rotation=30, ha="right")
    save_fig(out)


def plot_nodes_backtracks(df: pd.DataFrame, out: Path) -> None:
    data = df[df["solved"]].groupby("algo", as_index=False).agg(
        avg_nodes=("nodes", "mean"),
        avg_backtracks=("backtracks", "mean"),
    )
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    sns.barplot(data=data, x="algo", y="avg_nodes", ax=axes[0])
    axes[0].set_title("Average Nodes")
    axes[0].tick_params(axis="x", rotation=30)

    sns.barplot(data=data, x="algo", y="avg_backtracks", ax=axes[1])
    axes[1].set_title("Average Backtracks")
    axes[1].tick_params(axis="x", rotation=30)

    save_fig(out)


def plot_time_by_size(df: pd.DataFrame, out: Path) -> None:
    data = df[df["solved"]].groupby(["n", "algo"], as_index=False)["time_ms"].mean()
    if data.empty:
        return
    sns.lineplot(data=data, x="n", y="time_ms", hue="algo", marker="o")
    plt.title("Average Solve Time by Size (n)")
    save_fig(out)


def to_markdown_percent(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    data = df.copy()
    for col in columns:
        if col in data.columns:
            data[col] = (data[col] * 100).round(2)
    return data


def write_report(
    runs_path: Path,
    manifest_path: Path,
    output_path: Path,
    figdir: Path,
    df_runs: pd.DataFrame,
    df_features: pd.DataFrame,
) -> None:
    overview = dataset_overview(df_runs, df_features)
    size_dist = size_distribution(df_features)
    summary = aggregate_global(df_runs)
    by_source = aggregate_by_source(df_runs)
    by_size = aggregate_by_size(df_runs)
    rel = relative_vs_dlx(df_runs)
    ablation = ablation_backtracking(df_runs)

    dlx_corr = correlate_features(df_features, df_runs, "dlx", "time_ms")
    timeout_corr = correlate_features(df_features, df_runs, "baseline", "timeout")
    bias = bias_check(df_features)
    system = system_metadata()
    hard_profile = features_profile(df_features, df_runs, "baseline", top_k=25)

    source_counts = df_features.groupby("source", as_index=False)["puzzle_id"].count().rename(
        columns={"puzzle_id": "puzzles"}
    )

    md = [
        "# Queens Data Science Report",
        "",
        "## Dataset Overview",
        f"- Runs: {overview['runs']}",
        f"- Unique puzzles: {overview['unique_puzzles']}",
        f"- Source distribution: {overview['sources']}",
    ]

    if "solution_status" in overview:
        md.append(f"- Solution status: {overview['solution_status']}")

    md.extend(
        [
            "",
            "### Size Distribution",
            "",
            source_counts.to_markdown(index=False),
            "",
            size_dist.to_markdown(index=False),
            "",
            f"![Size Distribution](figures/{(figdir / 'size_distribution.png').name})",
            "",
        ]
    )

    md.extend(
        [
            "## Global Performance Summary",
            "",
            to_markdown_percent(summary, ["solved_rate", "timeout_rate"]).to_markdown(index=False),
            "",
            "## Performance by Source",
            "",
            to_markdown_percent(by_source, ["solved_rate", "timeout_rate"]).to_markdown(index=False),
        ]
    )

    md.append("")
    md.append("## Per-Size Performance Tables")
    for size in sorted(by_size["n"].unique()):
        subset = by_size[by_size["n"] == size]
        subset = to_markdown_percent(subset, ["solved_rate", "timeout_rate"])
        md.extend(["", f"### n = {int(size)}", "", subset.to_markdown(index=False)])

    md.extend(
        [
            "",
            "## Relative Performance vs DLX",
            "",
            to_markdown_percent(rel, ["delta_solve_rate"]).to_markdown(index=False) if not rel.empty else "_DLX runs missing_",
        ]
    )

    md.extend(
        [
            "",
            "## LCV Ablation (backtracking_bb_nolcv vs backtracking_bb)",
            "",
            ablation.to_markdown(index=False) if not ablation.empty else "_Ablation runs missing_",
        ]
    )

    md.extend(
        [
            "",
        "## Puzzle Feature Correlations",
        "",
        "### Correlation with DLX time (Spearman)",
        "",
        dlx_corr.head(15).to_markdown(index=False) if not dlx_corr.empty else "_No data_",
        "",
        "### Correlation with baseline timeouts (Spearman)",
        "",
        timeout_corr.head(15).to_markdown(index=False) if not timeout_corr.empty else "_No data_",
        "",
        "### Hard puzzles profile (baseline top-25)",
        "",
        hard_profile.head(15).to_markdown(index=False) if not hard_profile.empty else "_No data_",
    ]
    )

    md.extend(
        [
            "",
            "## Hardest Puzzles (per algorithm)",
        ]
    )
    for algo in sorted(set(df_runs["algo"]) - {"dlx"}):
        top = hardest_puzzles(df_runs, algo, top_k=10)
        if top.empty:
            continue
        md.extend(["", f"### {algo}", "", top.to_markdown(index=False)])

    md.extend(
        [
            "",
            "## Bias Check: generated vs imported",
            "",
            bias.to_markdown(index=False),
        ]
    )

    md.extend(
        [
            "",
            "## Charts",
            "",
            f"![Size Distribution](figures/{(figdir / 'size_distribution.png').name})",
            f"![Average Time](figures/{(figdir / 'avg_time.png').name})",
            f"![Solve Rate](figures/{(figdir / 'solve_rate.png').name})",
            f"![Time Distribution](figures/{(figdir / 'time_box.png').name})",
            f"![Nodes vs Backtracks](figures/{(figdir / 'nodes_backtracks.png').name})",
            f"![Average Time by Size](figures/{(figdir / 'time_by_size.png').name})",
            f"![Solve Rate by Size](figures/{(figdir / 'solve_rate_by_size.png').name})",
            f"![Median Time by Size](figures/{(figdir / 'per_size_median_time.png').name})",
            f"![Per-Size Solve Rate](figures/{(figdir / 'per_size_solve_rate.png').name})",
        ]
    )

    md.extend(
        [
            "",
            "## Methodology",
            "",
            "- solved: `solved == True` in runs JSONL",
            "- timeout: `timeout == True` in runs JSONL",
            "- time percentiles: computed on solved-only unless noted",
            f"- runs source file: `{runs_path}`",
            f"- puzzle manifest: `{manifest_path}`",
            f"- python: {system['python']}",
            f"- platform: {system['platform']}",
            f"- processor: {system['processor']}",
        ]
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an actionable Queens report.")
    parser.add_argument(
        "--runs",
        type=Path,
        default=Path("data/benchmarks/queens_runs.jsonl"),
        help="Path to runs JSONL.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/queens_unique.json"),
        help="Puzzle manifest with regions and sources.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("reports/queens_report.md"),
        help="Markdown output path.",
    )
    parser.add_argument(
        "--figdir",
        type=Path,
        default=Path("reports/figures"),
        help="Directory for PNG figures.",
    )
    args = parser.parse_args()

    matplotlib.use("Agg")
    sns.set_theme(style="whitegrid")
    ensure_dir(args.figdir)

    manifest = load_manifest(args.manifest)
    df_features = build_features_df(manifest)
    df_runs = load_runs(args.runs, drop_algos={"min_conflicts"})

    size_dist = size_distribution(df_features)
    plot_size_distribution(size_dist, args.figdir / "size_distribution.png")
    per_size = aggregate_by_size(df_runs)
    plot_median_time_by_size(per_size, args.figdir / "per_size_median_time.png")
    plot_solve_rate_by_size(per_size, args.figdir / "per_size_solve_rate.png")
    plot_avg_time(df_runs, args.figdir / "avg_time.png")
    plot_solve_rate(df_runs, args.figdir / "solve_rate.png")
    plot_time_box(df_runs, args.figdir / "time_box.png")
    plot_nodes_backtracks(df_runs, args.figdir / "nodes_backtracks.png")
    plot_time_by_size(df_runs, args.figdir / "time_by_size.png")
    plot_solve_rate_by_size(per_size, args.figdir / "solve_rate_by_size.png")

    write_report(args.runs, args.manifest, args.out, args.figdir, df_runs, df_features)

    print(f"Report written to: {args.out}")
    print(f"Figures written to: {args.figdir}")


if __name__ == "__main__":
    main()
