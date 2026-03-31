from __future__ import annotations

from typing import TYPE_CHECKING

import cv2

from config import (
    COLOR_EMPTY,
    COLOR_OCCUPIED,
    COLOR_PERSON,
    COLOR_POINT,
    PREVIEW_WINDOW_NAME,
)
from detector import get_people_boxes
from errors import CantOpenVideo, exit_with_err_description
from geometry import get_bottom_center_point, is_table_occupied_by_person
from tracker import TableEvent, TableEventType, TableState, TableTracker

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


def process_video(video_path: str, roi: Rect, show_preview: bool = False) -> list[TableEvent]:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise CantOpenVideo(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    x, y, w, h = roi

    # colors BGR
    COLOR_EMPTY = (0, 255, 0)
    COLOR_OCCUPIED = (0, 0, 255)
    COLOR_PERSON = (255, 0, 0)
    COLOR_POINT = (0, 0, 255)

    print(f"Processing video: {video_path}")
    if show_preview:
        print("Preview mode ENABLED. Press 'q' to stop.")
    else:
        print("Running in background mode (faster)...")

    window_name = "Analytics process"
    tracker = TableTracker()
    frame_count = 0
    cached_boxes = []
    events: list[TableEvent] = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % 15 == 0:
            cached_boxes = get_people_boxes(frame)

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        is_anyone_in_zone = False

        for box in cached_boxes:
            if is_table_occupied_by_person(roi, box):
                is_anyone_in_zone = True

        event = tracker.update(is_anyone_in_zone, current_time)
        if event is not None:
            events.append(event)
            print(f"\n[{event.timestamp:.1f}s] Event: {event.type.value}")

        
        if frame_count % 500 == 0:
            print(f"\rProcessed {frame_count}/{total_frames} ({frame_count * 100 // total_frames}%) frames...", end="")

        frame_count += 1

        if not show_preview:
            continue

        for box in cached_boxes:
            x1, y1, x2, y2 = box

            # Bottom-Center Point (BCP) coordinates
            bcp_xy = get_bottom_center_point((x1, y1, x2, y2))

            cv2.rectangle(frame, (x1, y1), (x2, y2), COLOR_PERSON, 2)

            # Draw BCP, -1 makes it filled
            cv2.circle(frame, bcp_xy, 5, COLOR_POINT, -1)

        table_color = (
            COLOR_EMPTY if tracker.table_state == TableState.EMPTY else COLOR_OCCUPIED
        )
        cv2.rectangle(frame, (x, y), (x + w, y + h), table_color, 2)
        text = f"STATE: {tracker.table_state.value}"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, table_color, 2)

        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    if show_preview:
        cv2.destroyWindow(window_name)

    cap.release()

    return events
