from __future__ import annotations

import json
from pathlib import Path

from linkedin_game_solver.cli import main
from linkedin_game_solver.games.queens.generator import generate_puzzle_payload


def _write_puzzle(path: Path, n: int, seed: int) -> None:
    payload, _solution = generate_puzzle_payload(n=n, seed=seed)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_cli_organize_dataset_moves_files(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir(parents=True)

    _write_puzzle(input_dir / "puzzle_a.json", n=6, seed=1)
    _write_puzzle(input_dir / "puzzle_b.json", n=7, seed=2)

    outdir = tmp_path / "out"
    exit_code = main(
        [
            "organize-dataset",
            "--game",
            "queens",
            "--input",
            str(input_dir),
            "--outdir",
            str(outdir),
            "--mode",
            "move",
        ]
    )
    assert exit_code == 0

    assert not list(input_dir.glob("*.json"))
    assert (outdir / "size_6" / "puzzle_a.json").exists()
    assert (outdir / "size_7" / "puzzle_b.json").exists()
