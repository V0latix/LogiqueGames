#!/usr/bin/env python3
"""Crop and deskew grid images for every chosen_frame in zip_archive/candidates.

This is a candidates-driven variant of scripts/04_crop_deskew_grid.py.
It reads `index_candidates.json` (entries with paths.chosen_frame) and writes a
new grids directory, so you can iterate on cropping without touching the old grids.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from config import (
    APPROX_EPSILON_RATIO,
    CANNY_HIGH,
    CANNY_LOW,
    MORPH_CLOSE_KERNEL,
    QUAD_MIN_AREA_RATIO,
    TARGET_WIDTH,
)
from pipeline_utils import dump_json, ensure_dir, load_json, relative_to_cwd, utc_now_iso


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crop and deskew candidate chosen frames")
    parser.add_argument("--index", default="zip_archive/metadata/index_candidates.json")
    parser.add_argument("--output-metadata", default="zip_archive/metadata/grid_results_candidates_v2.json")
    parser.add_argument("--grids-dir", default="zip_archive/grids_v2")
    parser.add_argument("--target-width", type=int, default=TARGET_WIDTH)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--only-video", default=None, help="Process only a specific video basename")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def order_points(pts: np.ndarray) -> np.ndarray:
    rect = np.zeros((4, 2), dtype="float32")
    sums = pts.sum(axis=1)
    rect[0] = pts[np.argmin(sums)]
    rect[2] = pts[np.argmax(sums)]

    diffs = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diffs)]
    rect[3] = pts[np.argmax(diffs)]
    return rect


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
    gaps = [b - a for a, b in zip(lines[:-1], lines[1:]) if 35 <= (b - a) <= 260]
    if not gaps:
        return lines
    step = float(np.median(np.array(gaps, dtype=np.float32)))
    if step <= 10:
        return lines
    offset = float(np.median([value % step for value in lines]))
    start = offset
    while start - step >= -0.5 * step:
        start -= step
    lattice: list[float] = []
    value = start
    while value <= axis_limit + 0.5 * step:
        lattice.append(value)
        value += step
    supported = [value for value in lattice if any(abs(obs - value) <= 0.35 * step for obs in lines)]
    if len(supported) < 3:
        return lines
    first, last = min(supported), max(supported)
    dense: list[float] = []
    value = first
    while value <= last + 1e-6:
        dense.append(value)
        value += step
    return dense


def detect_grid_lines(gray: np.ndarray) -> tuple[list[float], list[float]]:
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blur, 30, 100)
    h, w = gray.shape[:2]

    all_h: list[float] = []
    all_v: list[float] = []
    for threshold in (25, 35, 45, 55):
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi / 180,
            threshold=threshold,
            minLineLength=60,
            maxLineGap=4,
        )
        if lines is None:
            continue
        for x1, y1, x2, y2 in lines[:, 0]:
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


def _hough_bbox_quad(blur: np.ndarray, image_shape: tuple[int, int, int]) -> tuple[np.ndarray | None, float]:
    h_img, w_img = image_shape[:2]
    edges2 = cv2.Canny(blur, max(1, int(CANNY_LOW * 0.6)), max(2, int(CANNY_HIGH * 0.6)))
    lines = cv2.HoughLinesP(
        edges2,
        rho=1,
        theta=np.pi / 180,
        threshold=60,
        minLineLength=80,
        maxLineGap=6,
    )
    if lines is None:
        return None, 0.0
    all_h: list[float] = []
    all_v: list[float] = []
    for x1, y1, x2, y2 in lines[:, 0]:
        angle = abs(np.degrees(np.arctan2((y2 - y1), (x2 - x1))))
        angle = min(angle, 180.0 - angle)
        if angle < 10:
            all_h.append((y1 + y2) / 2.0)
        elif angle > 80:
            all_v.append((x1 + x2) / 2.0)
    if len(all_h) < 6 or len(all_v) < 6:
        return None, 0.0
    x0, x1 = np.percentile(np.array(all_v, dtype=np.float32), [5, 95]).tolist()
    y0, y1 = np.percentile(np.array(all_h, dtype=np.float32), [5, 95]).tolist()
    pad_x = 0.03 * max(1.0, (x1 - x0))
    pad_y = 0.03 * max(1.0, (y1 - y0))
    x0 = max(0.0, x0 - pad_x)
    y0 = max(0.0, y0 - pad_y)
    x1 = min(float(w_img - 1), x1 + pad_x)
    y1 = min(float(h_img - 1), y1 + pad_y)
    quad2 = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], dtype="float32")
    area2 = float((x1 - x0) * (y1 - y0))
    return quad2, area2 / float(h_img * w_img)


def find_best_quad(image: np.ndarray) -> tuple[np.ndarray | None, str, float]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, CANNY_LOW, CANNY_HIGH)

    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, MORPH_CLOSE_KERNEL)
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, close_kernel)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, "no_contours", 0.0

    image_area = image.shape[0] * image.shape[1]
    min_area = image_area * QUAD_MIN_AREA_RATIO

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    h_img, w_img = image.shape[:2]
    cx_img, cy_img = w_img / 2.0, h_img / 2.0

    quads: list[tuple[np.ndarray, str, float]] = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue

        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, APPROX_EPSILON_RATIO * perimeter, True)
        if len(approx) != 4:
            continue
        quad = approx.reshape(4, 2).astype("float32")
        area_ratio = float(area) / float(image_area)
        quads.append((quad, "quad", area_ratio))
        if len(quads) >= 12:
            # Keep only the largest few contours.
            break

    hough_quad, hough_ratio = _hough_bbox_quad(blur, image.shape)
    if hough_quad is not None:
        quads.append((hough_quad, "hough_bbox", hough_ratio))

    # Always include a bounding-rect fallback.
    largest = contours[0]
    x, y, w, h = cv2.boundingRect(largest)
    rect_pts = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], dtype="float32")
    rect_ratio = float(cv2.contourArea(largest)) / float(image_area)
    quads.append((rect_pts, "bounding_rect", rect_ratio))

    # Evaluate candidates by how well they expose a regular grid when warped.
    best: tuple[int, int, float, np.ndarray, str] | None = None
    for quad, method, area_ratio in quads:
        warped = warp_from_quad(image, quad)
        normalized = resize_to_width(warped, TARGET_WIDTH)
        gray_warp = cv2.cvtColor(normalized, cv2.COLOR_BGR2GRAY)
        xs, ys = detect_grid_lines(gray_warp)
        n = min(len(xs), len(ys)) - 1
        if n < 2:
            continue
        # Prefer larger inferred grids, then better supported line counts, then area.
        support = min(len(xs), len(ys))
        score = (int(n), int(support), float(area_ratio), quad, method)
        if best is None or score[:3] > best[:3]:
            best = score

    if best is not None:
        _n, _support, ratio, quad, method = best
        return quad, method, ratio

    return None, "no_candidate", 0.0


def warp_from_quad(image: np.ndarray, quad: np.ndarray) -> np.ndarray:
    rect = order_points(quad)
    tl, tr, br, bl = rect

    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = int(max(width_a, width_b))

    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = int(max(height_a, height_b))

    max_width = max(max_width, 2)
    max_height = max(max_height, 2)

    dst = np.array(
        [[0, 0], [max_width - 1, 0], [max_width - 1, max_height - 1], [0, max_height - 1]],
        dtype="float32",
    )

    matrix = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, matrix, (max_width, max_height))


def resize_to_width(image: np.ndarray, target_width: int) -> np.ndarray:
    h, w = image.shape[:2]
    if w <= 0 or h <= 0:
        return image
    if w == target_width:
        return image
    ratio = target_width / float(w)
    target_height = max(2, int(h * ratio))
    return cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_CUBIC)


def main() -> int:
    args = parse_args()

    index_path = Path(args.index)
    output_metadata = Path(args.output_metadata)
    grids_dir = Path(args.grids_dir)

    ensure_dir(grids_dir)
    ensure_dir(output_metadata.parent)

    index_payload = load_json(index_path, default={})
    entries = index_payload.get("entries", [])
    if not isinstance(entries, list):
        entries = []

    if args.only_video:
        entries = [e for e in entries if isinstance(e, dict) and e.get("video_basename") == args.only_video]

    if args.limit is not None:
        entries = entries[: args.limit]

    previous = load_json(output_metadata, default={})
    previous_by_basename = {
        e.get("video_basename"): e for e in previous.get("videos", []) if isinstance(e, dict) and e.get("video_basename")
    }

    output_entries: list[dict[str, Any]] = []

    for idx, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            continue
        basename = entry.get("video_basename")
        if not basename:
            continue

        chosen_value = (entry.get("paths") or {}).get("chosen_frame") if isinstance(entry.get("paths"), dict) else None
        frame_path = Path(str(chosen_value or ""))
        if not frame_path.is_absolute():
            frame_path = Path.cwd() / frame_path

        grid_path = grids_dir / f"{basename}_grid.png"

        prev = previous_by_basename.get(basename)
        if grid_path.exists() and prev and not args.force:
            output_entries.append(prev)
            if args.verbose:
                print(f"[{idx}/{len(entries)}] {basename}: skip (grid already exists)")
            continue

        if args.verbose:
            print(f"[{idx}/{len(entries)}] processing {basename}")

        if not frame_path.exists():
            output_entries.append(
                {
                    "video_basename": basename,
                    "chosen_frame": relative_to_cwd(frame_path),
                    "grid_image": relative_to_cwd(grid_path),
                    "status": "needs_review",
                    "error": "chosen frame does not exist",
                }
            )
            continue

        image = cv2.imread(str(frame_path), cv2.IMREAD_COLOR)
        if image is None:
            output_entries.append(
                {
                    "video_basename": basename,
                    "chosen_frame": relative_to_cwd(frame_path),
                    "grid_image": relative_to_cwd(grid_path),
                    "status": "needs_review",
                    "error": "unable to read frame",
                }
            )
            continue

        quad, method, area_ratio = find_best_quad(image)
        if quad is None:
            output_entries.append(
                {
                    "video_basename": basename,
                    "chosen_frame": relative_to_cwd(frame_path),
                    "grid_image": relative_to_cwd(grid_path),
                    "status": "needs_review",
                    "method": method,
                    "area_ratio": area_ratio,
                    "error": "grid contour not found",
                }
            )
            continue

        warped = warp_from_quad(image, quad)
        normalized = resize_to_width(warped, args.target_width)
        ensure_dir(grid_path.parent)
        cv2.imwrite(str(grid_path), normalized)

        status = "ok" if method == "quad" and area_ratio >= QUAD_MIN_AREA_RATIO else "needs_review"

        output_entries.append(
            {
                "video_basename": basename,
                "chosen_frame": relative_to_cwd(frame_path),
                "grid_image": relative_to_cwd(grid_path),
                "status": status,
                "method": method,
                "area_ratio": round(float(area_ratio), 5),
                "error": None,
            }
        )

    payload = {
        "generated_at": utc_now_iso(),
        "settings": {"target_width": args.target_width, "limit": args.limit},
        "videos": sorted(
            output_entries,
            key=lambda item: (
                item.get("video_basename", ""),
            ),
        ),
    }
    dump_json(output_metadata, payload)
    print(f"Wrote candidates grid metadata: {output_metadata} (videos={len(output_entries)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
