from cv2.typing import MatLike
import numpy
from ultralytics import YOLO  # type: ignore

from config import CONFIDENCE_THRESHOLD, IMAGE_SIZE, MODEL_NAME, PEOPLE_CLASSES


model = YOLO(MODEL_NAME)


def get_people_boxes(frame: MatLike) -> list[numpy.ndarray]:
    results = model(
        frame,
        classes=PEOPLE_CLASSES,
        conf=CONFIDENCE_THRESHOLD,
        imgsz=IMAGE_SIZE,
        verbose=False,
    )

    boxes = results[0].boxes
    if boxes is None:
        return []

    return [box.xyxy[0].cpu().numpy().astype(int) for box in boxes]
