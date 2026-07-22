"""Stage 1: Illumination auditing.

Edge detection and color segmentation are both unreliable on badly lit
images, so the pipeline audits illumination first and rejects images
early rather than producing misleading downstream metrics.
"""
import logging
from typing import Tuple

import cv2
import numpy as np

from .config import IlluminationConfig

logger = logging.getLogger(__name__)


def audit_illumination(
    image: np.ndarray, config: IlluminationConfig
) -> Tuple[bool, float]:
    """Evaluate whether an image has acceptable illumination.

    Uses the mean of the HSV "Value" channel as a proxy for overall
    brightness.

    Args:
        image: BGR image as loaded by ``cv2.imread``.
        config: Brightness thresholds to apply.

    Returns:
        A tuple ``(approved, brightness)`` where ``approved`` indicates
        whether the image passed the audit and ``brightness`` is the
        measured mean brightness (0-255).
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    brightness = float(np.mean(hsv[:, :, 2]))

    approved = config.min_brightness <= brightness <= config.max_brightness

    if not approved:
        logger.warning("Illumination rejected (brightness=%.2f)", brightness)

    return approved, brightness
