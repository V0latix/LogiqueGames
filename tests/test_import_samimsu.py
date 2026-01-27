from __future__ import annotations

from pathlib import Path

from linkedin_game_solver.games.queens.importers.samimsu import import_samimsu_dataset
from linkedin_game_solver.games.queens.parser import parse_puzzle_file


def _write_level_file(path: Path) -> None:
    content = """
const level = {
  size: 4,
  colorRegions: [
    ["A", "A", "B", "B"],
    ["A", "A", "B", "B"],
    ["C", "C", "D", "D"],
    ["C", "C", "D", "D"],
  ],
};
export default level;
"""
    path.write_text(content.strip(), encoding="utf-8")


def test_import_samimsu_dataset(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    levels_dir = repo_root / "src" / "utils" / "community-levels"
    levels_dir.mkdir(parents=True)

    level_path = levels_dir / "level1.ts"
    _write_level_file(level_path)

    outdir = tmp_path / "out"
    stats = import_samimsu_dataset(repo_root, outdir, on_invalid="skip")
    assert stats.total_files == 1
    assert stats.imported == 1
    assert stats.skipped == 0

    output_path = outdir / "samimsu_level1.json"
    assert output_path.exists()

    puzzle = parse_puzzle_file(output_path)
    assert puzzle.n == 4
