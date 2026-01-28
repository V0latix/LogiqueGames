"""Generate a data-science report with PNG charts from benchmark runs."""

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


def load_runs(path: Path) -> pd.DataFrame:
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    if not records:
        raise ValueError(f"No records found in {path}")
    return pd.DataFrame.from_records(records)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_fig(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def compute_summary(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("algo", as_index=False)
    summary = grouped.agg(
        puzzles=("algo", "count"),
        solved=("solved", "sum"),
        solved_rate=("solved", "mean"),
        avg_time_ms=("time_ms", lambda s: s[df.loc[s.index, "solved"]].mean()),
        median_time_ms=("time_ms", lambda s: s[df.loc[s.index, "solved"]].median()),
        avg_nodes=("nodes", lambda s: s[df.loc[s.index, "solved"]].mean()),
        avg_backtracks=("backtracks", lambda s: s[df.loc[s.index, "solved"]].mean()),
        timeout_rate=("timeout", "mean"),
    )
    summary = summary.sort_values(by=["avg_time_ms", "solved_rate"], ascending=[True, False])
    return summary


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


def plot_solve_rate_by_size(df: pd.DataFrame, out: Path) -> None:
    data = df.groupby(["n", "algo"], as_index=False)["solved"].mean()
    if data.empty:
        return
    sns.lineplot(data=data, x="n", y="solved", hue="algo", marker="o")
    plt.title("Solve Rate by Size (n)")
    plt.ylabel("solve_rate")
    save_fig(out)


def build_report(
    df: pd.DataFrame,
    summary: pd.DataFrame,
    input_path: Path,
    figdir: Path,
    report_path: Path,
) -> None:
    total_runs = len(df)
    puzzles = df["puzzle_id"].nunique()
    algos = ", ".join(summary["algo"].tolist())

    table = summary.copy()
    table["solved_rate"] = (table["solved_rate"] * 100).round(2)
    table["timeout_rate"] = (table["timeout_rate"] * 100).round(2)

    md = [
        "# Queens Data Science Report",
        "",
        f"- Source: `{input_path}`",
        f"- Runs: {total_runs}",
        f"- Unique puzzles: {puzzles}",
        f"- Algorithms: {algos}",
        "",
        "## Summary Table",
        "",
        table.to_markdown(index=False),
        "",
        "## Charts",
        "",
        f"![Average Time](figures/{(figdir / 'avg_time.png').name})",
        f"![Solve Rate](figures/{(figdir / 'solve_rate.png').name})",
        f"![Time Distribution](figures/{(figdir / 'time_box.png').name})",
        f"![Nodes vs Backtracks](figures/{(figdir / 'nodes_backtracks.png').name})",
        f"![Time by Size](figures/{(figdir / 'time_by_size.png').name})",
        f"![Solve Rate by Size](figures/{(figdir / 'solve_rate_by_size.png').name})",
    ]

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate DS report from benchmark runs JSONL.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/benchmarks/queens_runs.jsonl"),
        help="Path to JSONL runs file.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("reports/queens_report.md"),
        help="Path to report markdown.",
    )
    parser.add_argument(
        "--figdir",
        type=Path,
        default=Path("reports/figures"),
        help="Directory for PNG figures.",
    )

    args = parser.parse_args()

    df = load_runs(args.input)
    summary = compute_summary(df)

    sns.set_theme(style="whitegrid")
    ensure_dir(args.figdir)

    plot_avg_time(df, args.figdir / "avg_time.png")
    plot_solve_rate(df, args.figdir / "solve_rate.png")
    plot_time_box(df, args.figdir / "time_box.png")
    plot_nodes_backtracks(df, args.figdir / "nodes_backtracks.png")
    plot_time_by_size(df, args.figdir / "time_by_size.png")
    plot_solve_rate_by_size(df, args.figdir / "solve_rate_by_size.png")

    build_report(df, summary, args.input, args.figdir, args.out)

    print(f"Report written to: {args.out}")
    print(f"Figures written to: {args.figdir}")


if __name__ == "__main__":
    main()
