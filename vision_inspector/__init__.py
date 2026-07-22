"""Industrial Vision Inspector - automated visual QA pipeline built with OpenCV."""

__version__ = "2.0.0"

from .config import InspectionConfig
from .pipeline import ImageLoadError, inspect_image
from .report import InspectionReport

__all__ = [
    "InspectionConfig",
    "InspectionReport",
    "ImageLoadError",
    "inspect_image",
]
