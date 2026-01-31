from __future__ import annotations

import pandas as pd

from linkedin_game_solver.benchmarks import report_utils


def test_percentile_basic() -> None:
    series = pd.Series([1, 2, 3, 4, 5])
    assert report_utils.percentile(series, 50) == 3.0
    assert report_utils.percentile(series, 90) == 4.6


def test_gini_and_cv() -> None:
    values = [1, 1, 1, 1]
    assert report_utils.gini(values) == 0.0
    assert report_utils.coeff_variation(values) == 0.0


def test_aggregate_by_size() -> None:
    df = pd.DataFrame(
        [
            {"puzzle_id": 1, "algo": "a", "n": 5, "time_ms": 10, "solved": True, "nodes": 5, "timeout": False},
            {"puzzle_id": 2, "algo": "a", "n": 5, "time_ms": 20, "solved": True, "nodes": 7, "timeout": False},
            {"puzzle_id": 3, "algo": "b", "n": 6, "time_ms": 30, "solved": False, "nodes": 9, "timeout": True},
        ]
    )
    agg = report_utils.aggregate_by_size(df)
    row = agg[(agg["n"] == 5) & (agg["algo"] == "a")].iloc[0]
    assert row["puzzles"] == 2
    assert row["solved"] == 2
    assert row["median_time_ms_solved"] == 15
    assert row["median_time_ms_all"] == 15
