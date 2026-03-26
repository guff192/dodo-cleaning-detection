from cv2.typing import MatLike
import numpy
from ultralytics import YOLO  # type: ignore


model = YOLO("yolov8n.pt")

def get_people_boxes(frame: MatLike) -> list[numpy.ndarray]:
    results = model(frame, classes=[0], conf=0.08, imgsz=480, verbose=False)

    boxes = results[0].boxes 
    if boxes is None:
        return []

    return [box.xyxy[0].cpu().numpy().astype(int) for box in boxes]
