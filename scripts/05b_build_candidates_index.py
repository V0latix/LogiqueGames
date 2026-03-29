#!/usr/bin/env python3
"""Build an index.json-like file from zip_archive/candidates/*/chosen_frame.png.

This is useful when you want to run the grid → puzzle extraction over *all* candidate
frames (not only the subset present in selected_frames.json / index.json).
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from pipeline_utils import (
    dump_json,
    ensure_dir,
    extract_puzzle_date_from_title,
    extract_puzzle_number_from_title,
    infer_decreasing_dates_by_index,
    relative_to_cwd,
    utc_now_iso,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build index entries from candidates folder")
    parser.add_argument("--candidates-dir", default="zip_archive/candidates")
    parser.add_argument("--grids-dir", default="zip_archive/grids")
    parser.add_argument("--raw-videos-dir", default="zip_archive/raw_videos")
    parser.add_argument("--out", default="zip_archive/metadata/index_candidates.json")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--only-video", default=None, help="Process only a specific video_basename")
    return parser.parse_args()


def _parse_playlist_index(basename: str) -> int | None:
    prefix = basename.split("_", 1)[0]
    if prefix.isdigit():
        try:
            return int(prefix)
        except ValueError:
            return None
    return None


def _parse_video_id(basename: str) -> str | None:
    # Most downloaded YouTube assets look like: 011_<videoId>_<title...>
    parts = basename.split("_")
    if len(parts) >= 2 and len(parts[1]) == 11:
        return parts[1]
    return None


def main() -> int:
    args = parse_args()

    candidates_dir = Path(args.candidates_dir)
    grids_dir = Path(args.grids_dir)
    raw_videos_dir = Path(args.raw_videos_dir)
    out_path = Path(args.out)

    ensure_dir(out_path.parent)

    chosen_frames = sorted(candidates_dir.glob("*/chosen_frame.png"), key=lambda p: p.parent.name)
    entries: list[dict[str, Any]] = []

    for frame_path in chosen_frames:
        basename = frame_path.parent.name
        if args.only_video and basename != args.only_video:
            continue

        title = basename.replace("_", " ")
        playlist_index = _parse_playlist_index(basename)
        video_id = _parse_video_id(basename)
        puzzle_number = extract_puzzle_number_from_title(title)
        puzzle_date = extract_puzzle_date_from_title(title)

        raw_video = raw_videos_dir / f"{basename}.mp4"
        grid_image = grids_dir / f"{basename}_grid.png"

        entry: dict[str, Any] = {
            "video_basename": basename,
            "video_id": video_id,
            "title": title,
            "puzzle_number": puzzle_number,
            "puzzle_date": puzzle_date,
            "upload_date": None,
            "playlist_index": playlist_index,
            "source_url": None,
            "frame_timestamp": None,
            "paths": {
                "raw_video": relative_to_cwd(raw_video) if raw_video.exists() else None,
                "chosen_frame": relative_to_cwd(frame_path),
                "grid_image": relative_to_cwd(grid_image) if grid_image.exists() else None,
            },
            "status": "ok" if frame_path.exists() else "needs_review",
            "notes": [],
        }
        if entry["paths"]["grid_image"] is None:
            entry["status"] = "needs_review"
            entry["notes"].append("missing grid_image")

        entries.append(entry)
        if args.limit is not None and len(entries) >= args.limit:
            break

    # Fill missing dates when playlist_index is available and at least some dates were parsed.
    infer_decreasing_dates_by_index(entries)

    entries.sort(
        key=lambda item: (
            item.get("playlist_index") is None,
            item.get("playlist_index") or 10**9,
            item.get("video_basename", ""),
        )
    )

    payload = {
        "generated_at": utc_now_iso(),
        "count": len(entries),
        "entries": entries,
    }
    dump_json(out_path, payload)
    print(f"Wrote candidates index: {out_path} (entries={len(entries)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

