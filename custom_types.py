import numpy as np


RectXYXY = tuple[int, int, int, int]
"""
Rectangle in the form (x1, y1, x2, y2) 

The first pair of coordinates is for top left corner,
the second pair is for bottom right corner.
"""

RectXYWH = tuple[int, int, int, int]
"""
Rectangle in the form (x1, y1, width, height) 

The first pair of numbers are the x and y coordinates for top left corner,
the second pair are width and height of the rectangle.
"""

PointXY = tuple[int, int]
"""
Point in the form (x, y)
"""


def ndarray_to_rect_xyxy(array: np.ndarray) -> RectXYXY:
    return array[0], array[1], array[2], array[3]
