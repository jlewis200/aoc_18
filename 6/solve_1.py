#!/usr/bin/env python3

import re
from dataclasses import dataclass
from collections import defaultdict
import pandas as pd
from itertools import pairwise
import numpy as np


def solve(data):
    """ """
    data = np.array(data)
    buffer = data.max() - data.min()

    min_coord = data.min() - buffer
    max_coord = data.max() + buffer

    distances = {}

    for x in range(min_coord, max_coord):
        for y in range(min_coord, max_coord):
            point_distances = []

            for coord_x, coord_y in data:
                point_distance = abs(coord_y - y) + abs(coord_x - x)
                point_distances.append(point_distance)

            min_distance = min(point_distances)
            value_counts = dict(zip(*np.unique(point_distances, return_counts=True)))

            if value_counts[min_distance] > 1:
                distances[(x, y)] = -1
            else:
                distances[(x, y)] = np.argmin(point_distances)

    infinite = detect_infinite(distances)

    for x in range(min_coord, max_coord):
        for y in range(min_coord, max_coord):
            if distances[(x, y)] in infinite:
                del distances[(x, y)]

    value_counts = np.unique(list(distances.values()), return_counts=True)
    return value_counts[1].max()


def detect_infinite(distances):
    min_coord = np.min(list(distances))
    max_coord = np.max(list(distances))
    infinite = set()

    for coord in range(min_coord, max_coord + 1):
        infinite.add(distances[(coord, min_coord)])
        infinite.add(distances[(coord, max_coord)])
        infinite.add(distances[(min_coord, coord)])
        infinite.add(distances[(max_coord, coord)])

    return infinite


def parse(data):
    """ """
    return [tuple(map(int, line.strip().split(","))) for line in data]


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 17)
    main("input.txt")
