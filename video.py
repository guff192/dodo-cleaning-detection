from __future__ import annotations
from typing import TYPE_CHECKING
import cv2

from errors import exit_with_err_description

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
