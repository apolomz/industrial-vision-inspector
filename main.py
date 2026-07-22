#!/usr/bin/env python3
"""Command-line entry point for the Industrial Vision Inspector.

Usage:
    python main.py                          # inspect everything in input_images/
    python main.py path/to/image.png        # inspect a single image
    python main.py path/to/folder -v        # inspect a folder, verbose logging
"""
import argparse
import glob
import logging
import os
import sys

from vision_inspector.config import InspectionConfig
from vision_inspector.pipeline import ImageLoadError, inspect_image

IMAGE_PATTERNS = ("*.png", "*.jpg", "*.jpeg", "*.bmp")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Industrial Vision Inspector - automated visual QA pipeline."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="input_images",
        help="Path to an image file or a directory of images (default: input_images/)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="output_results",
        help="Directory for processed debug images (default: output_results/)",
    )
    parser.add_argument(
        "-r",
        "--reports-dir",
        default="reports",
        help="Directory for JSON reports, one per image (default: reports/)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    return parser


def collect_images(input_path: str):
    """Resolve ``input_path`` to a list of image files to process."""
    if os.path.isdir(input_path):
        files = []
        for pattern in IMAGE_PATTERNS:
            files.extend(glob.glob(os.path.join(input_path, pattern)))
        return sorted(files)
    return [input_path]


def main(argv=None) -> int:
    args = build_arg_parser().parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger("vision_inspector.cli")

    images = collect_images(args.input)
    if not images:
        logger.error("No images found at '%s'", args.input)
        return 1

    os.makedirs(args.reports_dir, exist_ok=True)
    config = InspectionConfig(output_dir=args.output_dir)

    exit_code = 0
    for image_path in images:
        try:
            report = inspect_image(image_path, config=config)
        except ImageLoadError as exc:
            logger.error(str(exc))
            exit_code = 1
            continue

        report_name = os.path.splitext(os.path.basename(image_path))[0]
        report_path = os.path.join(args.reports_dir, f"{report_name}.json")
        report.save(report_path)

        status_icon = "OK" if report.estado_auditoria == "APROBADO" else "RECHAZADA"
        logger.info("[%s] %s -> %s", status_icon, image_path, report_path)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
