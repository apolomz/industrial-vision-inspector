from vision_inspector.config import IlluminationConfig
from vision_inspector.illumination import audit_illumination


def test_dark_image_is_rejected(dark_image):
    approved, brightness = audit_illumination(dark_image, IlluminationConfig())
    assert not approved
    assert brightness < IlluminationConfig().min_brightness


def test_overexposed_image_is_rejected(overexposed_image):
    approved, brightness = audit_illumination(overexposed_image, IlluminationConfig())
    assert not approved
    assert brightness > IlluminationConfig().max_brightness


def test_well_lit_image_is_approved(bright_green_object_image):
    approved, brightness = audit_illumination(
        bright_green_object_image, IlluminationConfig()
    )
    assert approved
    config = IlluminationConfig()
    assert config.min_brightness <= brightness <= config.max_brightness
