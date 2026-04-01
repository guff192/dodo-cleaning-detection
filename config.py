# colors BGR
COLOR_EMPTY = (0, 255, 0)
COLOR_OCCUPIED = (0, 0, 255)
COLOR_PERSON = (255, 0, 0)
COLOR_POINT = (0, 0, 255)

# window names
PREVIEW_WINDOW_NAME = "Analytics process"

# detector settings
MODEL_NAME = "yolov8n.pt"
PEOPLE_CLASSES = [0]
CONFIDENCE_THRESHOLD = 0.15
IMAGE_SIZE = 480
SKIP_FRAMES = 15
MIN_INTERSECTION_RATIO = 0.5

# tracker settings
T_ENTER = 2.0
T_EXIT = 30.0
