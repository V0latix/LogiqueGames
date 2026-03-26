#!/usr/bin/env python3
"""Convert extracted Queens grid PNGs into JSON puzzles compatible with the repo Queens format.

Output schema per puzzle JSON:
{
  "game": "queens",
  "n": 8,
  "regions": [[0,0,1,...], ...],   # n×n matrix of region IDs (0-indexed)
  "givens": {"queens": [], "blocked": []},
  "meta": { ... }
}
"""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import cv2
import numpy as np
from pipeline_utils import dump_json, ensure_dir, load_json, relative_to_cwd, utc_now_iso


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert grid PNGs to Queens JSON puzzles")
    parser.add_argument("--index", default="zip_archive/metadata/index.json")
    parser.add_argument("--out-dir", default="zip_archive/puzzles_queens")
    parser.add_argument("--manifest", default="zip_archive/metadata/puzzles_queens_manifest.json")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


# ─── Grid line detection (shared logic with 06_grids_to_zip_puzzles) ──────────

def cluster_positions(values: list[float], eps: float = 8.0) -> list[float]:
    if not values:
        return []
    values = sorted(values)
    clusters: list[list[float]] = []
    for value in values:
        if not clusters or abs(value - clusters[-1][-1]) > eps:
            clusters.append([value])
        else:
            clusters[-1].append(value)
    return [float(sum(cluster) / len(cluster)) for cluster in clusters]


def regularize_line_spacing(lines: list[float], axis_limit: int) -> list[float]:
    if len(lines) < 3:
        return lines
    lines = sorted(lines)
    gaps = [b - a for a, b in zip(lines[:-1], lines[1:], strict=False) if 35 <= (b - a) <= 260]
    if not gaps:
        return lines
    step = float(np.median(np.array(gaps, dtype=np.float32)))
    if step <= 10:
        return lines
    offset = float(np.median([v % step for v in lines]))
    start = offset
    while start - step >= -0.5 * step:
        start -= step
    lattice: list[float] = []
    v = start
    while v <= axis_limit + 0.5 * step:
        lattice.append(v)
        v += step
    supported = [v for v in lattice if any(abs(obs - v) <= 0.35 * step for obs in lines)]
    if len(supported) < 3:
        return lines
    first, last = min(supported), max(supported)
    dense: list[float] = []
    v = first
    while v <= last + 1e-6:
        dense.append(v)
        v += step
    return dense


def detect_grid_lines(gray: np.ndarray) -> tuple[list[float], list[float]]:
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blur, 30, 100)
    h, w = gray.shape[:2]
    all_h: list[float] = []
    all_v: list[float] = []
    for threshold in (25, 35, 45, 55):
        lines = cv2.HoughLinesP(
            edges, rho=1, theta=np.pi / 180, threshold=threshold,
            minLineLength=60, maxLineGap=4,
        )
        if lines is None:
            continue
        for line in lines[:, 0]:
            x1, y1, x2, y2 = line
            angle = abs(np.degrees(np.arctan2((y2 - y1), (x2 - x1))))
            angle = min(angle, 180.0 - angle)
            if angle < 8:
                all_h.append((y1 + y2) / 2.0)
            elif angle > 82:
                all_v.append((x1 + x2) / 2.0)
    ys = cluster_positions(all_h, eps=7.0)
    xs = cluster_positions(all_v, eps=7.0)
    xs = regularize_line_spacing(xs, axis_limit=w)
    ys = regularize_line_spacing(ys, axis_limit=h)
    return xs, ys


# ─── Color-based region extraction ───────────────────────────────────────────

def sample_cell_colors(
    image: np.ndarray,
    xs: list[float],
    ys: list[float],
    n: int,
    margin_ratio: float = 0.25,
) -> np.ndarray:
    """Sample the median BGR color of each cell interior, avoiding grid-line borders.

    Returns an (n*n, 3) float32 array.
    """
    colors: list[list[float]] = []
    for r in range(n):
        for c in range(n):
            x0, x1 = int(xs[c]), int(xs[c + 1])
            y0, y1 = int(ys[r]), int(ys[r + 1])
            mx = max(2, int((x1 - x0) * margin_ratio))
            my = max(2, int((y1 - y0) * margin_ratio))
            cell = image[y0 + my : y1 - my, x0 + mx : x1 - mx]
            if cell.size == 0:
                colors.append([128.0, 128.0, 128.0])
            else:
                med = np.median(cell.reshape(-1, 3), axis=0)
                colors.append(med.tolist())
    return np.array(colors, dtype=np.float32)


def cluster_to_regions(colors: np.ndarray, n: int) -> tuple[list[list[int]], float]:
    """K-means (k=n) color clustering → n×n regions matrix.

    Region IDs are assigned in reading order (first occurrence, top-left to bottom-right)
    so they stay consistent across similar puzzles.

    Returns (regions, compactness) where low compactness = well-separated colors = good extraction.
    """
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.5)
    compactness, labels, _ = cv2.kmeans(
        colors, n, None, criteria, 10, cv2.KMEANS_PP_CENTERS,
    )
    label_flat = labels.flatten()

    remap: dict[int, int] = {}
    next_id = 0
    for lbl in label_flat:
        lbl = int(lbl)
        if lbl not in remap:
            remap[lbl] = next_id
            next_id += 1

    regions = [
        [remap[int(label_flat[r * n + c])] for c in range(n)]
        for r in range(n)
    ]
    return regions, float(compactness)


def non_contiguous_regions(regions: list[list[int]], n: int) -> list[int]:
    """Return IDs of regions whose cells are not all 4-connected (extraction artifact)."""
    bad: list[int] = []
    for region_id in range(n):
        cells = [(r, c) for r in range(n) for c in range(n) if regions[r][c] == region_id]
        if not cells:
            bad.append(region_id)
            continue
        visited: set[tuple[int, int]] = set()
        queue: deque[tuple[int, int]] = deque([cells[0]])
        while queue:
            r, c = queue.popleft()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and regions[nr][nc] == region_id and (nr, nc) not in visited:
                    queue.append((nr, nc))
        if len(visited) != len(cells):
            bad.append(region_id)
    return bad


# ─── File naming ─────────────────────────────────────────────────────────────

def output_filename(entry: dict, fallback_idx: int) -> str:
    puzzle_number = entry.get("puzzle_number")
    num_part = f"#{puzzle_number:03d}" if isinstance(puzzle_number, int) else "#unknown"
    date_part = str(entry.get("puzzle_date") or "date_unknown")
    basename = str(entry.get("video_basename") or f"video_{fallback_idx:03d}")
    return f"{num_part}_{date_part}__{basename}.json"


def puzzle_name(entry: dict) -> str | None:
    puzzle_number = entry.get("puzzle_number")
    puzzle_date = entry.get("puzzle_date")
    if isinstance(puzzle_number, int) and isinstance(puzzle_date, str) and puzzle_date:
        return f"Queens #{puzzle_number} - {puzzle_date}"
    if isinstance(puzzle_number, int):
        return f"Queens #{puzzle_number}"
    return None


# ─── Per-entry conversion ─────────────────────────────────────────────────────

def convert_one(entry: dict, out_dir: Path, force: bool = False) -> dict:
    grid_path_value = entry.get("paths", {}).get("grid_image")
    if not grid_path_value:
        return {
            "video_basename": entry.get("video_basename"),
            "status": "needs_review",
            "error": "missing grid path",
        }

    grid_path = Path(grid_path_value)
    if not grid_path.is_absolute():
        grid_path = Path.cwd() / grid_path

    file_name = output_filename(entry, fallback_idx=int(entry.get("playlist_index") or 0))
    out_path = out_dir / file_name

    if out_path.exists() and not force:
        return {
            "video_basename": entry.get("video_basename"),
            "playlist_index": entry.get("playlist_index"),
            "grid_image": relative_to_cwd(grid_path),
            "json_path": relative_to_cwd(out_path),
            "status": "ok",
            "skipped": True,
        }

    image = cv2.imread(str(grid_path), cv2.IMREAD_COLOR)
    if image is None:
        return {
            "video_basename": entry.get("video_basename"),
            "playlist_index": entry.get("playlist_index"),
            "grid_image": relative_to_cwd(grid_path),
            "status": "needs_review",
            "error": "cannot read grid image",
        }

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    xs, ys = detect_grid_lines(gray)
    n = min(len(xs), len(ys)) - 1

    if n < 2:
        return {
            "video_basename": entry.get("video_basename"),
            "playlist_index": entry.get("playlist_index"),
            "grid_image": relative_to_cwd(grid_path),
            "status": "needs_review",
            "error": f"unable to infer grid size ({len(xs)=}, {len(ys)=})",
        }

    colors = sample_cell_colors(image, xs, ys, n)
    regions, compactness = cluster_to_regions(colors, n)
    bad_regions = non_contiguous_regions(regions, n)
    name = puzzle_name(entry)

    payload = {
        "game": "queens",
        "n": n,
        "regions": regions,
        "givens": {"queens": [], "blocked": []},
        "meta": {
            "video_id": entry.get("video_id"),
            "playlist_index": entry.get("playlist_index"),
            "puzzle_number": entry.get("puzzle_number"),
            "puzzle_date": entry.get("puzzle_date"),
            "source_url": entry.get("source_url"),
            "frame_timestamp": entry.get("frame_timestamp"),
            "grid_image": relative_to_cwd(grid_path),
            "name": name,
            "conversion": "png_to_queens_v1",
        },
    }

    ensure_dir(out_path.parent)
    dump_json(out_path, payload)

    status = "ok"
    reasons: list[str] = []
    if bad_regions:
        status = "needs_review"
        reasons.append(f"non-contiguous regions: {bad_regions}")

    return {
        "video_basename": entry.get("video_basename"),
        "playlist_index": entry.get("playlist_index"),
        "video_id": entry.get("video_id"),
        "puzzle_number": entry.get("puzzle_number"),
        "puzzle_date": entry.get("puzzle_date"),
        "grid_image": relative_to_cwd(grid_path),
        "json_path": relative_to_cwd(out_path),
        "n": n,
        "name": name,
        "color_compactness": round(compactness, 2),
        "non_contiguous_regions": bad_regions,
        "status": status,
        "notes": reasons,
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    args = parse_args()

    index_path = Path(args.index)
    out_dir = Path(args.out_dir)
    manifest_path = Path(args.manifest)

    ensure_dir(out_dir)
    ensure_dir(manifest_path.parent)

    index_payload = load_json(index_path, default={})
    entries = list(index_payload.get("entries", []))
    if args.limit is not None:
        entries = entries[: args.limit]

    if not entries:
        print(f"No entries in {index_path}")
        return 0

    results: list[dict] = []
    for idx, entry in enumerate(entries, start=1):
        result = convert_one(entry, out_dir=out_dir, force=args.force)
        results.append(result)
        if args.verbose:
            status = result.get("status")
            name = result.get("name") or entry.get("video_basename")
            print(f"[{idx}/{len(entries)}] {name} -> {status}")

    ok_count = sum(1 for item in results if item.get("status") == "ok")
    review_count = len(results) - ok_count

    payload = {
        "generated_at": utc_now_iso(),
        "source_index": str(index_path),
        "count": len(results),
        "ok": ok_count,
        "needs_review": review_count,
        "entries": sorted(
            results,
            key=lambda item: (
                item.get("playlist_index") is None,
                item.get("playlist_index") or 10**9,
                item.get("video_basename", ""),
            ),
        ),
    }

    dump_json(manifest_path, payload)
    print(f"Wrote puzzles manifest: {manifest_path} (ok={ok_count}, needs_review={review_count})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
