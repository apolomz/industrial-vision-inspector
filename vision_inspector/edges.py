"""Stage 2: Adaptive Canny edge detection.

Fixed Canny thresholds work for a single lighting condition but break as
soon as brightness or contrast shifts. Deriving the thresholds from the
image's median intensity keeps edge detection stable across a wider
range of real production-line images.
"""
from typing import Tuple

import cv2
import numpy as np

from .config import CannyConfig


def adaptive_canny(
    gray_image: np.ndarray, config: CannyConfig
) -> Tuple[np.ndarray, int, int]:
    """Detect edges using Canny with thresholds derived from the image median.

    Args:
        gray_image: Single-channel grayscale image.
        config: Blur kernel size and sigma multipliers for the thresholds.

    Returns:
        A tuple ``(edges, lower_threshold, upper_threshold)``.
    """
    blurred = cv2.GaussianBlur(gray_image, config.blur_kernel, 0)
    median = float(np.median(blurred))

    lower = int(max(0, (1 - config.lower_sigma) * median))
    upper = int(min(255, (1 + config.upper_sigma) * median))

    edges = cv2.Canny(blurred, lower, upper)

    return edges, lower, upper
