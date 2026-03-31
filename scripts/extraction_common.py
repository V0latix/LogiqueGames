#!/usr/bin/env python3
"""Shared helpers for multi-frame puzzle extraction."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import cv2
import numpy as np


def resolve_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def candidate_frame_paths(entry: dict, max_frames: int = 20) -> list[Path]:
    paths = entry.get("paths") if isinstance(entry.get("paths"), dict) else {}
    chosen = resolve_path(paths.get("chosen_frame") if isinstance(paths, dict) else None)
    if chosen is None:
        return []

    frames: list[Path] = []
    if chosen.exists():
        frames.append(chosen)

    candidate_dir = chosen.parent
    if candidate_dir.exists():
        for path in sorted(candidate_dir.glob("candidate_*.png")):
            if path not in frames:
                frames.append(path)

    return frames[: max(1, max_frames)]


def order_points(pts: np.ndarray) -> np.ndarray:
    rect = np.zeros((4, 2), dtype="float32")
    sums = pts.sum(axis=1)
    rect[0] = pts[np.argmin(sums)]
    rect[2] = pts[np.argmax(sums)]
    diffs = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diffs)]
    rect[3] = pts[np.argmax(diffs)]
    return rect


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
    if w <= 0 or h <= 0 or w == target_width:
        return image
    ratio = target_width / float(w)
    target_height = max(2, int(h * ratio))
    return cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_CUBIC)


def _hough_bbox_quad(blur: np.ndarray, image_shape: tuple[int, int, int]) -> tuple[np.ndarray | None, float]:
    h_img, w_img = image_shape[:2]
    edges = cv2.Canny(blur, 18, 80)
    lines = cv2.HoughLinesP(
        edges,
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
    quad = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], dtype="float32")
    area = float((x1 - x0) * (y1 - y0))
    return quad, area / float(h_img * w_img)


def find_best_quad(
    image: np.ndarray,
    line_detector: Callable[[np.ndarray], tuple[list[float], list[float]]],
    min_area_ratio: float = 0.08,
) -> tuple[np.ndarray | None, str, float]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 30, 100)
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, close_kernel)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, "no_contours", 0.0

    image_area = image.shape[0] * image.shape[1]
    min_area = image_area * min_area_ratio
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    quads: list[tuple[np.ndarray, str, float]] = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) != 4:
            continue
        quad = approx.reshape(4, 2).astype("float32")
        quads.append((quad, "quad", float(area) / float(image_area)))
        if len(quads) >= 12:
            break

    hough_quad, hough_ratio = _hough_bbox_quad(blur, image.shape)
    if hough_quad is not None:
        quads.append((hough_quad, "hough_bbox", hough_ratio))

    if not quads:
        x, y, w, h = cv2.boundingRect(contours[0])
        rect = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], dtype="float32")
        return rect, "bounding_rect", float(w * h) / float(image_area)

    best: tuple[int, int, float, np.ndarray, str] | None = None
    for quad, method, area_ratio in quads:
        warped = warp_from_quad(image, quad)
        gray_warp = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        xs, ys = line_detector(gray_warp)
        n = min(len(xs), len(ys)) - 1
        if n < 2:
            continue
        support = min(len(xs), len(ys))
        score = (int(n), int(support), float(area_ratio), quad, method)
        if best is None or score[:3] > best[:3]:
            best = score

    if best is not None:
        _n, _support, ratio, quad, method = best
        return quad, method, ratio

    quad, method, ratio = quads[0]
    return quad, method, ratio


def normalize_grid_from_frame(
    frame_path: Path,
    line_detector: Callable[[np.ndarray], tuple[list[float], list[float]]],
    target_width: int = 1200,
    min_area_ratio: float = 0.08,
) -> dict | None:
    image = cv2.imread(str(frame_path), cv2.IMREAD_COLOR)
    if image is None:
        return None

    quad, method, area_ratio = find_best_quad(image, line_detector=line_detector, min_area_ratio=min_area_ratio)
    if quad is None:
        return None

    warped = warp_from_quad(image, quad)
    normalized = resize_to_width(warped, target_width=target_width)
    gray = cv2.cvtColor(normalized, cv2.COLOR_BGR2GRAY)
    xs, ys = line_detector(gray)

    # Tight crop around the detected lattice to remove UI clutter before parsing.
    if len(xs) >= 3 and len(ys) >= 3:
        n = min(len(xs), len(ys)) - 1
        cell_w = max(2.0, float(xs[-1] - xs[0]) / max(1, n))
        cell_h = max(2.0, float(ys[-1] - ys[0]) / max(1, n))
        pad_x = 0.18 * cell_w
        pad_y = 0.18 * cell_h

        x0 = max(0, int(round(float(xs[0]) - pad_x)))
        x1 = min(normalized.shape[1], int(round(float(xs[-1]) + pad_x)))
        y0 = max(0, int(round(float(ys[0]) - pad_y)))
        y1 = min(normalized.shape[0], int(round(float(ys[-1]) + pad_y)))
        if x1 > x0 + 20 and y1 > y0 + 20:
            normalized = normalized[y0:y1, x0:x1]
            normalized = resize_to_width(normalized, target_width=target_width)
            gray = cv2.cvtColor(normalized, cv2.COLOR_BGR2GRAY)
            xs, ys = line_detector(gray)

    n = min(len(xs), len(ys)) - 1
    return {
        "image": normalized,
        "gray": gray,
        "xs": xs,
        "ys": ys,
        "n": int(n),
        "method": method,
        "area_ratio": float(area_ratio),
    }
