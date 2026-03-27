"""Tests for zip generator error paths and edge cases."""

from __future__ import annotations

import pytest

from linkedin_game_solver.games.zip.generator import (
    _choose_checkpoints,
    generate_zip_puzzle_payload,
)


# ── generate_zip_puzzle_payload error paths ──────────────────────────────────

def test_generator_n_too_small_raises() -> None:
    with pytest.raises(ValueError, match="n must be at least 2"):
        generate_zip_puzzle_payload(n=1)


def test_generator_max_walls_negative_raises() -> None:
    with pytest.raises(ValueError, match="max_walls must be >= 0"):
        generate_zip_puzzle_payload(n=3, max_walls=-1)


def test_generator_checkpoints_range_invalid_raises() -> None:
    with pytest.raises(ValueError, match="checkpoints_range must be positive"):
        generate_zip_puzzle_payload(n=3, checkpoints_range=(3, 1))


def test_generator_checkpoints_range_zero_raises() -> None:
    with pytest.raises(ValueError, match="checkpoints_range must be positive"):
        generate_zip_puzzle_payload(n=3, checkpoints_range=(0, 5))


def test_generator_max_attempts_exceeded_raises() -> None:
    with pytest.raises(ValueError, match="Failed to generate"):
        # ensure_unique=True with tiny time limit forces count_solutions to timeout every attempt
        generate_zip_puzzle_payload(
            n=3,
            seed=42,
            checkpoints=2,
            ensure_unique=True,
            max_attempts=1,
            unique_timelimit_s=0.000001,
        )


def test_generator_progress_every_runs() -> None:
    """progress_every triggers print but still succeeds."""
    result = generate_zip_puzzle_payload(
        n=3,
        seed=5,
        ensure_unique=False,
        max_attempts=5,
        progress_every=1,
    )
    assert result.payload is not None


# ── _choose_checkpoints edge cases ────────────────────────────────────────────

def test_choose_checkpoints_ratio_zero_raises() -> None:
    import random
    rng = random.Random(0)
    path = [(r, c) for r in range(3) for c in range(3)]
    with pytest.raises(ValueError, match="Checkpoint ratio must be between 0 and 1"):
        _choose_checkpoints(path, rng, 0.0, ensure_last=False)


def test_choose_checkpoints_ratio_one_raises() -> None:
    import random
    rng = random.Random(0)
    path = [(r, c) for r in range(3) for c in range(3)]
    with pytest.raises(ValueError, match="Checkpoint ratio must be between 0 and 1"):
        _choose_checkpoints(path, rng, 1.0, ensure_last=False)


def test_choose_checkpoints_count_zero_raises() -> None:
    import random
    rng = random.Random(0)
    path = [(r, c) for r in range(3) for c in range(3)]
    with pytest.raises(ValueError, match="Checkpoint count must be positive"):
        _choose_checkpoints(path, rng, 0, ensure_last=False)


def test_choose_checkpoints_count_one_no_ensure_last() -> None:
    """count=1 with ensure_last=False returns {1: first cell}."""
    import random
    rng = random.Random(0)
    path = [(r, c) for r in range(3) for c in range(3)]
    result = _choose_checkpoints(path, rng, 1, ensure_last=False)
    assert result == {1: (0, 0)}


def test_choose_checkpoints_ensure_last_forces_min_two() -> None:
    """ensure_last=True with count=1 bumps count to 2."""
    import random
    rng = random.Random(0)
    path = [(r, c) for r in range(3) for c in range(3)]
    result = _choose_checkpoints(path, rng, 1, ensure_last=True)
    # Should have at least 2 checkpoints: first and last
    assert len(result) >= 2
    assert path[0] in result.values()
    assert path[-1] in result.values()


def test_choose_checkpoints_too_many_requested_clamped() -> None:
    """Requesting more checkpoints than available pool is clamped."""
    import random
    rng = random.Random(0)
    path = [(r, c) for r in range(2) for c in range(2)]  # 4 cells
    # Ask for more than possible (pool = 2 interior cells, need 10)
    result = _choose_checkpoints(path, rng, 10, ensure_last=False)
    assert len(result) <= len(path)
