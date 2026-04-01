import cv2

from config import (
    COLOR_EMPTY,
    COLOR_OCCUPIED,
    COLOR_PERSON,
    COLOR_POINT,
    PREVIEW_WINDOW_NAME,
    SKIP_FRAMES,
    TIME_ENTER,
    TIME_EXIT,
)
from detector import get_people_boxes
from errors import CantOpenVideo, exit_with_err_description
from geometry import get_bottom_center_point, is_anyone_in_zone
from custom_types import RectXYWH, RectXYXY, ndarray_to_rect_xyxy
from logger import log_processing_info, log_progress
from tracker import TableEvent, TableEventType, TableState, TableTracker


def _get_state_at_time(current_time: float, events: list[TableEvent]) -> TableState:
    state = TableState.EMPTY
    for event in events:
        if not event.timestamp < current_time:
            break

        match event.type:
            case TableEventType.APPROACH:
                state = TableState.OCCUPIED
            case TableEventType.FREED:
                state = TableState.EMPTY

    return state


def _draw_preview_overlay(
    frame: cv2.typing.MatLike,
    roi: RectXYWH,
    people_boxes: list[RectXYXY],
    table_state: TableState,
):
    x, y, w, h = roi

    for box in people_boxes:
        x1, y1, x2, y2 = box

        cv2.rectangle(frame, (x1, y1), (x2, y2), COLOR_PERSON, 2)

        # Bottom-Center Point (BCP) coordinates
        bcp_xy = get_bottom_center_point((x1, y1, x2, y2))
        # Draw BCP, -1 thickness makes it filled
        cv2.circle(frame, bcp_xy, 5, COLOR_POINT, -1)

    table_color = COLOR_EMPTY if table_state == TableState.EMPTY else COLOR_OCCUPIED
    cv2.rectangle(frame, (x, y), (x + w, y + h), table_color, 2)

    text = f"STATE: {table_state.value}"
    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, table_color, 2)


def select_roi(video_path: str) -> RectXYWH:
    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()
    if not ret:
        cap.release()
        exit_with_err_description(f'Can\'t read the video "{video_path}"!')

    window_name = "Select ROI (Press ENTER/SPACE to confirm, 'c' to cancel)"
    roi = cv2.selectROI(window_name, frame, showCrosshair=True, fromCenter=False)

    cv2.destroyWindow(window_name)
    cap.release()

    if roi == (0, 0, 0, 0):
        exit_with_err_description("No ROI selected!")

    x, y, w, h = roi
    return x, y, w, h


def process_video(
    video_path: str, roi: RectXYWH, show_preview: bool = False
) -> list[TableEvent]:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise CantOpenVideo(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    log_processing_info(video_path, show_preview)

    window_name = PREVIEW_WINDOW_NAME
    tracker = TableTracker(t_enter=TIME_ENTER, t_exit=TIME_EXIT)
    frame_count = 0
    cached_boxes = []
    events: list[TableEvent] = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % SKIP_FRAMES == 0:
            cached_boxes = [
                ndarray_to_rect_xyxy(box) for box in get_people_boxes(frame)
            ]

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        frame_count += 1

        anyone_in_zone = is_anyone_in_zone(roi, cached_boxes)

        event = tracker.update(anyone_in_zone, current_time)
        if event is not None:
            events.append(event)
            print(f"\n[{event.timestamp:.1f}s] Event: {event.type.value}")

        log_progress(frame_count, total_frames)

        if not show_preview:
            continue

        _draw_preview_overlay(frame, roi, cached_boxes, tracker.table_state)
        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    if show_preview:
        cv2.destroyWindow(window_name)

    cap.release()

    return events


def render_output_video(video_path: str, output_path: str, events: list[TableEvent], roi: RectXYWH):
    print(f"\nRendering final video to {output_path}...")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise CantOpenVideo(video_path)

    # Video saving settings
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        table_state = _get_state_at_time(current_time, events)
        _draw_preview_overlay(frame, roi, [], table_state)

        frame_count += 1

        log_progress(frame_count, total_frames)
        out.write(frame)

    cap.release()
    out.release()

    print("\nDone!")
