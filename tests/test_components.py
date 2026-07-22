from vision_inspector.components import analyze_components
from vision_inspector.config import SegmentationConfig
from vision_inspector.segmentation import segment_object


def test_single_object_detected(bright_green_object_image):
    mask = segment_object(bright_green_object_image, SegmentationConfig())
    total, areas, avg_area = analyze_components(mask)

    assert total == 1
    assert len(areas) == 1
    assert avg_area == areas[0]


def test_empty_mask_has_zero_objects():
    import numpy as np

    empty_mask = np.zeros((100, 100), dtype=np.uint8)
    total, areas, avg_area = analyze_components(empty_mask)

    assert total == 0
    assert areas == []
    assert avg_area == 0.0


def test_min_area_filters_small_components():
    import cv2
    import numpy as np

    mask = np.zeros((100, 100), dtype=np.uint8)
    cv2.circle(mask, (20, 20), 3, 255, -1)  # tiny noise speck
    cv2.rectangle(mask, (50, 50), (80, 80), 255, -1)  # real object

    total_unfiltered, _, _ = analyze_components(mask, min_area=0)
    total_filtered, areas_filtered, _ = analyze_components(mask, min_area=100)

    assert total_unfiltered == 2
    assert total_filtered == 1
    assert areas_filtered[0] > 100
