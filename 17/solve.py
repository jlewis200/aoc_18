#!/usr/bin/env python3

import re
from time import sleep
import sys
from dataclasses import dataclass
from aoc_data_structures import VectorTuple

sys.setrecursionlimit(20000)


SRC = VectorTuple(0, 500)
DOWN = VectorTuple(1, 0)
LEFT = VectorTuple(0, -1)
RIGHT = VectorTuple(0, 1)
NULL = VectorTuple(0, 0)


@dataclass
class State:
    clay: set
    flowing_water: set
    stagnant_water: set
    visited: set
    y_min: int
    y_max: int
    animate: bool
    animation_delay: int


def solve(parsed):
    clay = get_clay_set(parsed)
    state = State(
        clay=clay,
        flowing_water={SRC},
        y_min=min(clay, key=lambda x: x[0])[0],
        y_max=max(clay, key=lambda x: x[0])[0],
        stagnant_water=set(),
        visited=set(),
        animate=False,
        animation_delay=0.1,
    )

    flow(state, SRC)
    return (
        len(list(filter_water(state, state.flowing_water | state.stagnant_water))),
        len(list(filter_water(state, state.stagnant_water))),
    )


def animate(state):
    if state.animate:
        print_grid(state)
        sleep(state.animation_delay)


def flow(state, drop):
    """
    DFS through open positions and flowing water.  Travel down if available.
    If not, attempt to travel left and right.
    """
    animate(state)
    state.visited.add(drop)

    if drop[0] > state.y_max:
        return False

    state.flowing_water.add(drop)
    next_drop = drop + DOWN

    if next_drop not in state.clay and next_drop not in state.visited:
        flow(state, next_drop)

    if next_drop in state.clay or next_drop in state.stagnant_water:
        left_terminal = flow_horizontal(state, drop + LEFT, LEFT)
        right_terminal = flow_horizontal(state, drop + RIGHT, RIGHT)

        if left_terminal and right_terminal:
            stagnate(state, drop)
            return True

    return False


def flow_horizontal(state, drop, delta):
    """
    Flow along horizontal axis.  If there is an opportunity to flow down,
    prioritize that.  After flowing down, continue horizontal flow if below is
    stagnant.
    """
    animate(state)
    state.visited.add(drop)

    if drop in state.clay or drop in state.stagnant_water:
        return True

    state.flowing_water.add(drop)
    next_drop = drop + DOWN

    if next_drop not in state.clay and next_drop not in state.visited:
        flow(state, next_drop)

        if next_drop in state.flowing_water:
            return False

    return flow_horizontal(state, drop + delta, delta)


def stagnate(state, drop):
    """
    Stagnate horizontally reachable water starting from drops.
    """
    for delta in (NULL, LEFT, RIGHT):
        next_drop = drop + delta

        while next_drop in state.flowing_water:
            animate(state)
            state.flowing_water.remove(next_drop)
            state.stagnant_water.add(next_drop)
            next_drop += delta


def filter_water(state, water):
    """
    Remove water outside y_min and y_max.
    """

    def filter_criteria(drop):
        return drop[0] in range(state.y_min, state.y_max + 1)

    return filter(filter_criteria, water)


def print_grid(state):
    combined = state.clay | state.flowing_water | state.stagnant_water
    x_min = min(combined, key=lambda x: x[1])[1]
    x_max = max(combined, key=lambda x: x[1])[1]
    grid = ""

    for y in range(state.y_min, state.y_max + 1):
        grid += f"{y:<10}"
        for x in range(x_min, x_max + 1):
            if VectorTuple(y, x) in state.flowing_water:
                grid += "|"
            elif VectorTuple(y, x) in state.stagnant_water:
                grid += "~"
            elif VectorTuple(y, x) in state.clay:
                grid += "#"
            else:
                grid += "."
        grid += "\n"
    print(grid)


def get_clay_set(parsed):
    """
    Map coordinates to types.
    """
    clay_set = set()

    for y_range, x_range in parsed:
        for y in y_range:
            for x in x_range:
                clay_set.add(VectorTuple(y, x))

    return clay_set


def get_range(dimension):
    if ".." in dimension:
        start, end = dimension.split("..")
        start, end = int(start), int(end) + 1
    else:
        start = int(dimension)
        end = start + 1
    return range(start, end)


def get_ranges(line):
    x = re.match(r".*x=(?P<x>[\d.]+)", line).group("x")
    y = re.match(r".*y=(?P<y>[\d.]+)", line).group("y")
    return get_range(y), get_range(x)


def parse(lines):
    parsed = []

    for line in lines:
        parsed.append(get_ranges(line))  # do something more useful here

    return parsed


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", (57, 29))
    main("input.txt")
