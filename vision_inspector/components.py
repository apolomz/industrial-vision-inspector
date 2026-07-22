"""Stage 4: Connected component analysis.

Turns a binary mask into per-object measurements (count, individual
areas, average area), which is the core signal used to decide whether a
part is present, missing, or fragmented.
"""
from typing import List, Tuple

import cv2
import numpy as np


def analyze_components(
    mask: np.ndarray, min_area: int = 0
) -> Tuple[int, List[int], float]:
    """Count and measure connected components (detected objects) in a binary mask.

    Args:
        mask: Single-channel binary mask (0 or 255).
        min_area: Components smaller than this (in pixels) are discarded,
            filtering out residual noise that survives morphological cleanup.

    Returns:
        A tuple ``(total_objects, areas, average_area)``.
    """
    num_labels, _labels, stats, _centroids = cv2.connectedComponentsWithStats(
        mask, connectivity=8
    )

    areas = [
        int(stats[i, cv2.CC_STAT_AREA])
        for i in range(1, num_labels)
        if stats[i, cv2.CC_STAT_AREA] >= min_area
    ]

    total_objects = len(areas)
    average_area = float(np.mean(areas)) if total_objects > 0 else 0.0

    return total_objects, areas, average_area
