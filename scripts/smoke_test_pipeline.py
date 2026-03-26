#!/usr/bin/env python3
"""Run a minimal smoke test of the extraction pipeline on one local video."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS_COMMON = [
    "scripts/02_extract_frames.py",
    "scripts/03_pick_best_frames.py",
    "scripts/04_crop_deskew_grid.py",
    "scripts/05_export_archive.py",
]

SCRIPTS_GAME: dict[str, list[str]] = {
    "zip": [
        "scripts/06_grids_to_zip_puzzles.py",
        "scripts/07_export_site_zip_format.py",
    ],
    "queens": [
        "scripts/06_grids_to_queens_puzzles.py",
        "scripts/07_export_site_queens_format.py",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke test on one local raw video")
    parser.add_argument("--game", choices=["zip", "queens"], default="zip")
    parser.add_argument("--fps", type=float, default=0.5)
    parser.add_argument("--start_offset", type=float, default=0.0)
    parser.add_argument("--end_offset", type=float, default=0.0)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def run(cmd: list[str], verbose: bool) -> None:
    if verbose:
        print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    args = parse_args()

    raw_videos = sorted(Path("zip_archive/raw_videos").glob("*.mp4"))
    if not raw_videos:
        print("No local videos found in zip_archive/raw_videos; smoke test skipped.")
        return 0

    print(f"Running smoke test ({args.game}) on first video: {raw_videos[0].name}")

    run(
        [
            sys.executable,
            SCRIPTS_COMMON[0],
            "--limit", "1",
            "--fps", str(args.fps),
            "--start_offset", str(args.start_offset),
            "--end_offset", str(args.end_offset),
            "--force",
        ],
        args.verbose,
    )
    run([sys.executable, SCRIPTS_COMMON[1], "--limit", "1", "--force"], args.verbose)
    run([sys.executable, SCRIPTS_COMMON[2], "--limit", "1", "--force"], args.verbose)
    run([sys.executable, SCRIPTS_COMMON[3], "--limit", "1", "--force"], args.verbose)

    for script in SCRIPTS_GAME[args.game]:
        run([sys.executable, script, "--limit", "1", "--force"], args.verbose)

    print(f"Smoke test ({args.game}) completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
