from enum import Enum
from dataclasses import dataclass


class TableState(str, Enum):
    EMPTY = "EMPTY"
    OCCUPIED = "OCCUPIED"


class TableEventType(str, Enum):
    APPROACH = "APPROACH"
    FREED = "FREED"


@dataclass(slots=True, frozen=True)
class TableEvent:
    type: TableEventType
    timestamp: float


class TableTracker:
    def __init__(self, t_enter: float = 2.0, t_exit: float = 30.0) -> None:
        self._state = TableState.EMPTY
        self._first_seen_time: float | None = None
        self._last_seen_time: float | None = None
        self._t_enter = t_enter
        self._t_exit = t_exit

    def update(self, is_person_in_zone: bool, current_time: float) -> TableEvent | None:
        match self._state:
            case TableState.EMPTY:
                if not is_person_in_zone:
                    self._first_seen_time = None
                    return

                if self._first_seen_time is None:
                    self._first_seen_time = current_time
                    return

                if current_time - self._first_seen_time >= self._t_enter:
                    self._state = TableState.OCCUPIED
                    self._last_seen_time = current_time
                    approach_time = self._first_seen_time
                    self._first_seen_time = None

                    return TableEvent(
                        type=TableEventType.APPROACH, timestamp=approach_time
                    )

            case TableState.OCCUPIED:
                if is_person_in_zone:
                    self._last_seen_time = current_time
                    return

                if self._last_seen_time is None:
                    self._last_seen_time = current_time
                    return

                if current_time - self._last_seen_time >= self._t_exit:
                    self._state = TableState.EMPTY
                    freed_time = self._last_seen_time
                    self._first_seen_time = None
                    self._last_seen_time = None

                    return TableEvent(type=TableEventType.FREED, timestamp=freed_time)

            case _:
                return
