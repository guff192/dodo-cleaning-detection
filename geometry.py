from errors import NonPositiveRectangleAreaException
from custom_types import RectXYWH, RectXYXY, PointXY


def is_anyone_in_zone(roi: RectXYWH, people_boxes: list[RectXYXY]) -> bool:
    for box in people_boxes:
        x1, y1, x2, y2 = box
        if is_table_occupied_by_person(roi, (x1, y1, x2, y2)):
            return True
    return False


def is_table_occupied_by_person(roi: RectXYWH, person_box: RectXYXY) -> bool:
    x, y, w, h = roi
    x1, y1, x2, y2 = person_box

    person_bcp = get_bottom_center_point((x1, y1, x2, y2))
    if not is_point_in_rect(person_bcp, (x, y, x + w, y + h)):
        return False

    if get_intersection_ratio((x, y, x + w, y + h), (x1, y1, x2, y2)) > 0.5:
        return False

    return True


def get_bottom_center_point(rect: RectXYXY) -> PointXY:
    bcp_x = (rect[0] + rect[2]) // 2
    bcp_y = rect[3]
    return bcp_x, bcp_y


def is_point_in_rect(point: PointXY, rect: RectXYXY) -> bool:
    rx1, ry1, rx2, ry2 = rect
    px, py = point
    return rx1 <= px <= rx2 and ry1 <= py <= ry2


def get_intersection_ratio(rect1: RectXYXY, rect2: RectXYXY) -> float:
    """Counts the ratio of intersection area of 2 rectangles to the area of the first rectangle"""
    x1_min, y1_min, x1_max, y1_max = rect1
    x2_min, y2_min, x2_max, y2_max = rect2

    rect1_area = (x1_max - x1_min) * (y1_max - y1_min)
    if rect1_area <= 0:
        raise NonPositiveRectangleAreaException

    # top-left & bottom-right points of intersection
    inters_tl = (max(x1_min, x2_min), max(y1_min, y2_min))
    inters_br = (min(x1_max, x2_max), min(y1_max, y2_max))

    if inters_tl[0] >= inters_br[0] or inters_tl[1] >= inters_br[1]:
        return 0

    inters_area = (inters_br[0] - inters_tl[0]) * (inters_br[1] - inters_tl[1])

    return inters_area / rect1_area
