from vision_inspector.config import SegmentationConfig
from vision_inspector.segmentation import segment_object


def test_segmentation_detects_green_square(bright_green_object_image):
    mask = segment_object(bright_green_object_image, SegmentationConfig())

    assert mask.shape == bright_green_object_image.shape[:2]
    assert mask.max() == 255

    # The square is 100x100 = 10,000 px; allow slack for morphology.
    detected_pixels = int((mask > 0).sum())
    assert 5000 < detected_pixels < 12000


def test_segmentation_finds_nothing_on_empty_background():
    import numpy as np

    background = np.full((100, 100, 3), (40, 40, 40), dtype=np.uint8)
    mask = segment_object(background, SegmentationConfig())
    assert mask.max() == 0
