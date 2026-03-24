from __future__ import annotations
from typing import TYPE_CHECKING
import argparse
import os
import os.path
import sys

import cv2

if TYPE_CHECKING:
    from cv2.typing import Rect


def select_roi(video_path: str) -> Rect:
    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()
    if not ret:
        cap.release()
        exit_with_err_description(f'Can\'t read the video "{video_path}"!')

    window_name = "Select ROI (Press ENTER/SPACE to confirm, 'c' to cancel)"
    roi = cv2.selectROI(window_name, frame, showCrosshair=True, fromCenter=False)

    cv2.destroyWindow(window_name)
    cap.release()

    return roi





def exit_with_err_description(description: str) -> None:
    print(description, file=sys.stderr)
    exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Detects time bounds of people interactions with tables from restaurant's camera video"
    )
    parser.add_argument("--video", type=str, required=True)

    args = parser.parse_args()
    video = args.video

    if not os.path.exists(video):
        full_path = os.path.join(os.getcwd(), video)
        exit_with_err_description(f'Video "{full_path}" does not exist!')

    print(f"Selected video: {video}")

    roi = select_roi(video)
    x, y, w, h = roi
    print(
        f"Selected table coordinates: upper-left corner: ({x}, {y}), width: {w}, height: {h}"
    )
