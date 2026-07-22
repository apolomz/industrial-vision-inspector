import cv2
import pytest

from vision_inspector.config import InspectionConfig
from vision_inspector.pipeline import ImageLoadError, inspect_image


def test_full_pipeline_approves_well_lit_image(tmp_path, bright_green_object_image):
    image_path = tmp_path / "sample.png"
    cv2.imwrite(str(image_path), bright_green_object_image)

    config = InspectionConfig(output_dir=str(tmp_path / "output"))
    report = inspect_image(str(image_path), config=config)

    assert report.estado_auditoria == "APROBADO"
    assert report.total_piezas_detectadas == 1
    assert report.umbral_inferior_canny is not None


def test_full_pipeline_rejects_dark_image(tmp_path, dark_image):
    image_path = tmp_path / "dark.png"
    cv2.imwrite(str(image_path), dark_image)

    config = InspectionConfig(output_dir=str(tmp_path / "output"))
    report = inspect_image(str(image_path), config=config)

    assert report.estado_auditoria == "RECHAZADO_ILUMINACION"
    assert report.total_piezas_detectadas is None


def test_missing_image_raises_image_load_error(tmp_path):
    with pytest.raises(ImageLoadError):
        inspect_image(str(tmp_path / "does_not_exist.png"))


def test_report_json_shape(tmp_path, bright_green_object_image):
    image_path = tmp_path / "sample.png"
    cv2.imwrite(str(image_path), bright_green_object_image)

    config = InspectionConfig(output_dir=str(tmp_path / "output"))
    report = inspect_image(str(image_path), config=config)

    data = report.to_dict()
    assert "deteccion_bordes" in data
    assert "segmentacion_objetos" in data
    assert data["segmentacion_objetos"]["total_piezas_detectadas"] == 1
