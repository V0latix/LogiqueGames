from __future__ import annotations

import json
from pathlib import Path

from linkedin_game_solver.cli import main
from linkedin_game_solver.games.queens.generator import generate_puzzle_payload


def _write_puzzle(path: Path, n: int, seed: int) -> None:
    payload, _solution = generate_puzzle_payload(n=n, seed=seed)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_bench_writes_runs_jsonl(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    _write_puzzle(input_dir / "a.json", n=6, seed=1)
    _write_puzzle(input_dir / "b.json", n=6, seed=2)

    manifest_path = tmp_path / "puzzles.json"
    main(
        [
            "export-dataset",
            "--input",
            str(input_dir),
            "--out",
            str(manifest_path),
            "--source",
            "imported",
        ]
    )

    runs_path = tmp_path / "runs.jsonl"
    report_path = tmp_path / "report.md"
    exit_code = main(
        [
            "bench",
            "--game",
            "queens",
            "--dataset",
            str(manifest_path),
            "--algo",
            "baseline,dlx",
            "--report",
            str(report_path),
            "--runs-out",
            str(runs_path),
        ]
    )
    assert exit_code == 0
    assert runs_path.exists()

    lines = runs_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 4
    sample = json.loads(lines[0])
    assert "algo" in sample
    assert "time_ms" in sample
