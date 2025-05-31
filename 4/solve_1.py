#!/usr/bin/env python3

import re
from dataclasses import dataclass
from collections import defaultdict
from datetime import datetime
import pandas as pd


@dataclass
class Event:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    event: str


def solve(data):
    """ """
    events = []

    for event in data:
        events.append(
            {
                "timestamp": datetime(
                    year=500 + event.year,
                    month=event.month,
                    day=event.day,
                    hour=event.hour,
                    minute=event.minute,
                ),
                "event": event.event,
            }
        )

    df = pd.DataFrame(events).set_index("timestamp")
    events = df["event"].sort_index()
    events.index = pd.DatetimeIndex(events.index)

    asleep_map = defaultdict(lambda: [])

    for timestamp, event in events.resample("1min").ffill().items():
        match = re.fullmatch(r"Guard #(?P<guard_id>\d+) begins shift", event)

        if match is not None:
            guard_id = int(match.group("guard_id"))
            awake = True

        elif event == "falls asleep":
            awake = False

        elif event == "wakes up":
            awake = True

        if not awake and timestamp.minute in range(0, 60):
            asleep_map[guard_id].append(timestamp.minute)

    asleep = pd.Series(asleep_map)
    guard_id = asleep.apply(len).idxmax()
    minute = pd.Series(asleep.loc[guard_id]).value_counts().idxmax()
    return guard_id * minute


def parse(data):
    """ """
    events = []

    for line in data:
        pattern = r"\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+)\] (?P<event>.+)"
        match = re.fullmatch(pattern, line.strip())
        events.append(
            Event(
                year=int(match.group("year")),
                month=int(match.group("month")),
                day=int(match.group("day")),
                hour=int(match.group("hour")),
                minute=int(match.group("minute")),
                event=match.group("event"),
            )
        )

    return events


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 240)
    main("input.txt")
