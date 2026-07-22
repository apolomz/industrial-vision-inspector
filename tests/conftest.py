"""Shared pytest fixtures.

Tests use synthetic, in-memory images instead of real photographs so the
suite is fast, deterministic, and doesn't require any binary assets to
be committed to the repository.
"""
import cv2
import numpy as np
import pytest


@pytest.fixture
def bright_green_object_image() -> np.ndarray:
    """A well-lit synthetic image with one solid green square (100x100 px)."""
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    img[:, :] = (40, 40, 40)  # dark gray background (BGR)
    cv2.rectangle(img, (50, 50), (150, 150), (0, 200, 0), -1)  # green square
    return img


@pytest.fixture
def dark_image() -> np.ndarray:
    """A fully black, underexposed image."""
    return np.zeros((100, 100, 3), dtype=np.uint8)


@pytest.fixture
def overexposed_image() -> np.ndarray:
    """A fully white, overexposed image."""
    return np.full((100, 100, 3), 255, dtype=np.uint8)
