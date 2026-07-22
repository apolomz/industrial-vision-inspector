"""Stage 3: HSV-based color segmentation.

Morphological opening removes small noise specks left by the color
threshold, and closing fills small holes inside otherwise-solid objects,
so the connected-components stage sees clean, whole shapes.
"""
import cv2
import numpy as np

from .config import SegmentationConfig


def segment_object(image: np.ndarray, config: SegmentationConfig) -> np.ndarray:
    """Segment the target object(s) from the background using an HSV color range.

    Args:
        image: BGR image as loaded by ``cv2.imread``.
        config: HSV bounds and morphology kernel sizes.

    Returns:
        A single-channel binary mask (0 or 255) of the same size as ``image``.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, config.lower_array(), config.upper_array())

    kernel_open = np.ones(config.open_kernel, np.uint8)
    kernel_close = np.ones(config.close_kernel, np.uint8)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)

    return mask
