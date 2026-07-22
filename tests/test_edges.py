import cv2

from vision_inspector.config import CannyConfig
from vision_inspector.edges import adaptive_canny


def test_adaptive_canny_detects_edges(bright_green_object_image):
    gray = cv2.cvtColor(bright_green_object_image, cv2.COLOR_BGR2GRAY)
    edges, lower, upper = adaptive_canny(gray, CannyConfig())

    assert edges.shape == gray.shape
    assert lower <= upper
    assert set(edges.reshape(-1).tolist()).issubset({0, 255})
    assert edges.max() == 255  # the square's border should produce edges
