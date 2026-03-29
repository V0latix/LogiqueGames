from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def _load_module():
    repo_root = Path(__file__).resolve().parents[1]
    scripts_dir = repo_root / "scripts"
    script_path = scripts_dir / "06b_gpt_vision_puzzles.py"

    # The script uses `from pipeline_utils import ...` which lives in scripts/.
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    spec = importlib.util.spec_from_file_location("gpt_vision_puzzles", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


MOD = _load_module()


def test_parse_gpt_response_clean_json() -> None:
    raw = '{"game":"queens","n":4,"regions":[[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3]]}'
    payload = MOD.parse_gpt_response(raw)
    assert payload["game"] == "queens"
    assert payload["n"] == 4


def test_parse_gpt_response_with_markdown_fences() -> None:
    raw = """```json
{"game":"zip","n":6,"numbers":[{"k":1,"r":0,"c":0},{"k":2,"r":5,"c":5}],"walls":[]}
```"""
    payload = MOD.parse_gpt_response(raw)
    assert payload["game"] == "zip"
    assert payload["n"] == 6


def test_validate_queens_ok() -> None:
    payload = {
        "game": "queens",
        "n": 4,
        "regions": [
            [0, 1, 2, 3],
            [0, 1, 2, 3],
            [0, 1, 2, 3],
            [0, 1, 2, 3],
        ],
    }
    MOD.validate_queens(payload)


def test_validate_queens_wrong_n() -> None:
    payload = {
        "game": "queens",
        "n": 4,
        "regions": [
            [0, 1, 2, 3],
            [0, 1, 2, 3],
            [0, 1, 2, 3],
        ],
    }
    with pytest.raises(ValueError, match="regions"):
        MOD.validate_queens(payload)


def test_validate_zip_ok() -> None:
    payload = {
        "game": "zip",
        "n": 6,
        "numbers": [{"k": 1, "r": 0, "c": 0}, {"k": 2, "r": 5, "c": 5}],
        "walls": [{"r1": 0, "c1": 0, "r2": 0, "c2": 1}],
    }
    MOD.validate_zip(payload)


def test_validate_zip_missing_k() -> None:
    payload = {
        "game": "zip",
        "n": 6,
        "numbers": [{"r": 0, "c": 0}, {"k": 2, "r": 5, "c": 5}],
        "walls": [],
    }
    with pytest.raises(ValueError, match=r"\.k"):
        MOD.validate_zip(payload)


def test_output_filename() -> None:
    entry = {"video_basename": "abc", "puzzle_number": 42, "puzzle_date": "2026-01-15"}
    assert MOD.output_filename(entry, fallback_idx=0) == "#042_2026-01-15__abc.json"
