"""Configuration objects for the industrial vision inspection pipeline.

Keeping every tunable value inside dataclasses (instead of scattered magic
numbers) makes it possible to adjust the pipeline for a different product
line, camera, or lighting rig without touching the algorithm code.
"""
from dataclasses import dataclass, field
from typing import Tuple

import numpy as np


@dataclass(frozen=True)
class IlluminationConfig:
    """Acceptable brightness range for the HSV Value channel (0-255)."""

    min_brightness: float = 40.0
    max_brightness: float = 220.0


@dataclass(frozen=True)
class CannyConfig:
    """Parameters for adaptive Canny edge detection."""

    blur_kernel: Tuple[int, int] = (5, 5)
    lower_sigma: float = 0.33
    upper_sigma: float = 0.33


@dataclass(frozen=True)
class SegmentationConfig:
    """HSV color range and morphology kernels used to isolate the target object.

    Defaults target green objects/parts. Override for other colors, e.g.
    red parts on a conveyor belt or blue plastic components.
    """

    hsv_lower: Tuple[int, int, int] = (35, 40, 40)
    hsv_upper: Tuple[int, int, int] = (90, 255, 255)
    open_kernel: Tuple[int, int] = (5, 5)
    close_kernel: Tuple[int, int] = (7, 7)

    def lower_array(self) -> np.ndarray:
        return np.array(self.hsv_lower, dtype=np.uint8)

    def upper_array(self) -> np.ndarray:
        return np.array(self.hsv_upper, dtype=np.uint8)


@dataclass(frozen=True)
class InspectionConfig:
    """Top-level configuration bundling every pipeline stage."""

    illumination: IlluminationConfig = field(default_factory=IlluminationConfig)
    canny: CannyConfig = field(default_factory=CannyConfig)
    segmentation: SegmentationConfig = field(default_factory=SegmentationConfig)
    min_component_area: int = 0
    output_dir: str = "output_results"
