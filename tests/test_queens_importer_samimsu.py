"""Tests for queens samimsu importer — coverage of error paths."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from linkedin_game_solver.games.queens.importers.samimsu import (
    ImportError,
    _extract_bracket_block,
    _extract_size,
    import_samimsu_dataset,
)


# ── _extract_bracket_block ────────────────────────────────────────────────────

def test_extract_bracket_block_key_not_found() -> None:
    with pytest.raises(ValueError, match="not found"):
        _extract_bracket_block("some text without key", "missingKey")


def test_extract_bracket_block_no_bracket_after_key() -> None:
    with pytest.raises(ValueError, match="No '\\['"):
        _extract_bracket_block("colorRegions: no bracket here", "colorRegions")


def test_extract_bracket_block_unterminated() -> None:
    with pytest.raises(ValueError, match="Unterminated"):
        _extract_bracket_block("colorRegions: [[1, 2", "colorRegions")


def test_extract_bracket_block_success() -> None:
    result = _extract_bracket_block('colorRegions: [[1, 2], [3, 4]]', "colorRegions")
    assert result == "[[1, 2], [3, 4]]"


# ── _extract_size ─────────────────────────────────────────────────────────────

def test_extract_size_not_found() -> None:
    with pytest.raises(ValueError, match="size not found"):
        _extract_size("no size here")


def test_extract_size_success() -> None:
    assert _extract_size("const size: 6") == 6


# ── import_samimsu_dataset — error paths ─────────────────────────────────────

def test_import_invalid_on_invalid_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="on_invalid must be"):
        import_samimsu_dataset(tmp_path, tmp_path / "out", on_invalid="raise")


def test_import_missing_levels_dir_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="levels directory not found"):
        import_samimsu_dataset(tmp_path, tmp_path / "out")


def _write_level_file(levels_dir: Path, name: str, content: str) -> None:
    levels_dir.mkdir(parents=True, exist_ok=True)
    (levels_dir / name).write_text(content, encoding="utf-8")


def _make_levels_dir(source_root: Path) -> Path:
    levels_dir = source_root / "src" / "utils" / "community-levels"
    levels_dir.mkdir(parents=True, exist_ok=True)
    return levels_dir


def test_import_wrong_dimensions_skipped(tmp_path: Path) -> None:
    """colorRegions with wrong row count is skipped."""
    levels_dir = _make_levels_dir(tmp_path)
    content = """
export const level1 = {
  size: 4,
  colorRegions: [["A","B","C","D"],["E","F","G","H"],["I","J","K","L"]],
};
"""
    _write_level_file(levels_dir, "level1.ts", content)
    stats = import_samimsu_dataset(tmp_path, tmp_path / "out", on_invalid="skip")
    assert stats.skipped == 1
    assert stats.imported == 0


def test_import_wrong_region_count_skipped(tmp_path: Path) -> None:
    """colorRegions where distinct colors != size is skipped."""
    levels_dir = _make_levels_dir(tmp_path)
    # 4x4 grid but only 3 distinct colors (A, B, C) instead of 4
    row = '["A","B","C","A"]'
    content = f"""
export const level2 = {{
  size: 4,
  colorRegions: [{row},{row},{row},{row}],
}};
"""
    _write_level_file(levels_dir, "level2.ts", content)
    stats = import_samimsu_dataset(tmp_path, tmp_path / "out", on_invalid="skip")
    assert stats.skipped == 1


def test_import_on_invalid_fail_raises_import_error(tmp_path: Path) -> None:
    """on_invalid='fail' raises ImportError on first bad file."""
    levels_dir = _make_levels_dir(tmp_path)
    # No size key → will fail extraction
    _write_level_file(levels_dir, "level3.ts", "export const level3 = { data: [] };")
    with pytest.raises(ImportError, match="Failed to import"):
        import_samimsu_dataset(tmp_path, tmp_path / "out", on_invalid="fail")


def test_import_valid_level_imported(tmp_path: Path) -> None:
    """A valid 4x4 level with 4 distinct colors is imported successfully."""
    levels_dir = _make_levels_dir(tmp_path)
    content = """
export const level4 = {
  size: 4,
  colorRegions: [
    ["A","A","B","B"],
    ["A","A","B","B"],
    ["C","C","D","D"],
    ["C","C","D","D"]
  ],
};
"""
    _write_level_file(levels_dir, "level4.ts", content)
    outdir = tmp_path / "out"
    stats = import_samimsu_dataset(tmp_path, outdir, on_invalid="skip")
    assert stats.imported == 1
    assert stats.skipped == 0
    assert (outdir / "samimsu_level4.json").exists()
