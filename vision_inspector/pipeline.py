"""Orchestrates the full inspection pipeline for a single image."""
import logging
import os
from typing import Optional

import cv2
import numpy as np

from .components import analyze_components
from .config import InspectionConfig
from .edges import adaptive_canny
from .illumination import audit_illumination
from .report import InspectionReport, utc_timestamp
from .segmentation import segment_object

logger = logging.getLogger(__name__)


class ImageLoadError(Exception):
    """Raised when an input image cannot be read from disk."""


def inspect_image(
    image_path: str,
    config: Optional[InspectionConfig] = None,
    save_debug_images: bool = True,
) -> InspectionReport:
    """Run the full inspection pipeline on a single image and return a report.

    Stages:
        1. Illumination audit (early rejection of under/overexposed images).
        2. Adaptive Canny edge detection.
        3. HSV color segmentation + morphological cleanup.
        4. Connected component analysis.

    Args:
        image_path: Path to the image file on disk.
        config: Pipeline configuration. Uses defaults if not provided.
        save_debug_images: Whether to write the edge map and mask to
            ``config.output_dir`` for visual inspection/debugging.

    Returns:
        The resulting :class:`InspectionReport`.

    Raises:
        ImageLoadError: If the image cannot be read (missing file,
            corrupted data, or unsupported format).
    """
    config = config or InspectionConfig()

    image = cv2.imread(image_path)
    if image is None:
        raise ImageLoadError(f"Could not read image: {image_path}")

    filename = os.path.basename(image_path)
    logger.info("Inspecting %s", filename)

    approved, brightness = audit_illumination(image, config.illumination)

    if not approved:
        return InspectionReport(
            archivo_procesado=filename,
            estado_auditoria="RECHAZADO_ILUMINACION",
            brillo_promedio_hsv=round(brightness, 2),
            timestamp_utc=utc_timestamp(),
        )

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges, lower, upper = adaptive_canny(gray, config.canny)

    mask = segment_object(image, config.segmentation)

    if save_debug_images:
        os.makedirs(config.output_dir, exist_ok=True)
        stem = os.path.splitext(filename)[0]
        cv2.imwrite(os.path.join(config.output_dir, f"bordes_{stem}.png"), edges)
        cv2.imwrite(os.path.join(config.output_dir, f"mascara_{stem}.png"), mask)

    edge_pct = float(np.count_nonzero(edges) / edges.size * 100)
    area_pct = float(np.count_nonzero(mask) / mask.size * 100)

    total_objects, areas, avg_area = analyze_components(
        mask, min_area=config.min_component_area
    )

    report = InspectionReport(
        archivo_procesado=filename,
        estado_auditoria="APROBADO",
        brillo_promedio_hsv=round(brightness, 2),
        timestamp_utc=utc_timestamp(),
        umbral_inferior_canny=lower,
        umbral_superior_canny=upper,
        porcentaje_pixeles_borde=round(edge_pct, 2),
        total_piezas_detectadas=total_objects,
        areas_individuales_pixeles=areas,
        porcentaje_area_ocupada=round(area_pct, 2),
        area_promedio_pieza_pixeles=round(avg_area, 2),
    )

    logger.info("Inspection complete for %s: %s", filename, report.estado_auditoria)

    return report
