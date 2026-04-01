import pandas as pd
from tracker import TableEvent, TableEventType


def print_statistics(events: list[TableEvent]) -> None:
    if len(events) < 2:
        print("Not enough data for analysis")
        return

    events_dict = {
        "timestamp": [event.timestamp for event in events],
        "type": [event.type.value for event in events],
    }
    df = pd.DataFrame(events_dict)
    df["duration"] = df["timestamp"].diff()
    new_approach_durations = df[df["type"] == TableEventType.APPROACH.value]["duration"]

    print(f"\nAverage approach duration: {new_approach_durations.mean()}")
