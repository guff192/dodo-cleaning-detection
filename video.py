from __future__ import annotations
from typing import TYPE_CHECKING
import cv2

from detector import get_people_boxes
from errors import exit_with_err_description
from geometry import get_bottom_center_point, is_table_occupied_by_person
from tracker import TableEventType, TableTracker

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


def run_preview(video_path: str, roi: Rect) -> None:
    cap = cv2.VideoCapture(video_path)
    x, y, w, h = roi
    table_color = (0, 255, 0)
    person_color = (255, 0, 0)
    point_color = (0, 0, 255)

    print("Starting video preview, press 'q' to quit...")

    window_name = "Video detection preview"
    tracker = TableTracker()
    frame_count = 0
    cached_boxes = []
    events = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % 15 == 0:
            cached_boxes = get_people_boxes(frame)

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        is_anyone_in_zone = False

        for box in cached_boxes:
            x1, y1, x2, y2 = box

            if is_table_occupied_by_person(roi, box):
                is_anyone_in_zone = True
                table_color = (0, 0, 255)

            cv2.rectangle(frame, (x1, y1), (x2, y2), person_color, 2)

            # Bottom-Center Point (BCP) coordinates
            bcp_xy = get_bottom_center_point((x1, y1, x2, y2))

            # Draw BCP, -1 makes it filled
            cv2.circle(frame, bcp_xy, 5, point_color, -1)

        event = tracker.update(is_anyone_in_zone, current_time)
        if event is not None:
            events.append(event)
            print(f"Table is {event.type.lower()} at {event.timestamp}")
            if event.type == TableEventType.FREED:
                table_color = (0, 255, 0)

        cv2.rectangle(frame, (x, y), (x + w, y + h), table_color, 2)
        text = "Table zone"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, table_color, 2)

        frame_count += 1

        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyWindow(window_name)
    cap.release()
