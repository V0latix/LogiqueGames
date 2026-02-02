from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from linkedin_game_solver.cli import _handle_generate_zip


def test_zip_cli_generate_writes_file(tmp_path: Path) -> None:
    args = Namespace(
        game="zip",
        n=3,
        seed=123,
        outdir=tmp_path,
        render=False,
        allow_multiple=False,
        unique_timelimit=0.5,
        checkpoints=None,
        checkpoint_ratio=None,
        checkpoints_range="3,5",
        max_attempts=10,
        path_timelimit=0.2,
        max_walls=2,
        progress_every=None,
    )
    exit_code = _handle_generate_zip(args)
    assert exit_code == 0
    assert (tmp_path / "zip_n3_seed123.json").exists()
