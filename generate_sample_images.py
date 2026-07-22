#!/usr/bin/env python3
"""Generate synthetic sample images so the project runs out of the box.

Real production-line photos are not included in this repository. Run
this script once to populate `input_images/` with a few synthetic
examples that exercise each branch of the pipeline: a well-lit part, an
underexposed frame, and a fragmented/defective part.
"""
import os

import cv2
import numpy as np


def _canvas(width=400, height=300, background=(40, 40, 40)):
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:, :] = background
    return img


def make_good_sample() -> np.ndarray:
    """A well-lit frame with three solid green parts."""
    img = _canvas()
    cv2.rectangle(img, (60, 60), (160, 160), (0, 200, 0), -1)
    cv2.circle(img, (280, 200), 60, (0, 180, 0), -1)
    cv2.rectangle(img, (250, 50), (330, 110), (0, 210, 0), -1)
    return img


def make_dark_sample() -> np.ndarray:
    """An underexposed frame that should be rejected by the illumination audit."""
    img = _canvas(background=(5, 5, 5))
    cv2.rectangle(img, (60, 60), (160, 160), (0, 20, 0), -1)
    return img


def make_defective_sample() -> np.ndarray:
    """A frame with small, fragmented green regions simulating a broken part."""
    img = _canvas()
    for cx, cy in [(80, 80), (95, 130), (150, 90), (300, 220)]:
        cv2.circle(img, (cx, cy), 8, (0, 200, 0), -1)
    return img


def main() -> None:
    output_dir = "input_images"
    os.makedirs(output_dir, exist_ok=True)

    samples = {
        "muestra_buena.png": make_good_sample(),
        "muestra_oscura.png": make_dark_sample(),
        "muestra_defectuosa.png": make_defective_sample(),
    }

    for filename, image in samples.items():
        path = os.path.join(output_dir, filename)
        cv2.imwrite(path, image)
        print(f"Created {path}")


if __name__ == "__main__":
    main()
