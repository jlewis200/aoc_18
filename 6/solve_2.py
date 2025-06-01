#!/usr/bin/env python3

import re
from dataclasses import dataclass
from collections import defaultdict, deque
import pandas as pd
from itertools import pairwise
import numpy as np


def solve(data, threshold):
    """ """
    data = np.array(data)
    center = data.mean(axis=0).astype(int)

    visited = {tuple(center)}
    queue = deque([center])
    safe_area_size = 0

    while len(queue) > 0:
        coord = queue.popleft()
        distance = abs((coord - data)).sum()

        if distance < threshold:
            safe_area_size += 1

            for delta in [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ]:
                adjacency = coord + delta

                if tuple(adjacency) not in visited:
                    queue.append(adjacency)
                    visited.add(tuple(adjacency))

    print(safe_area_size)
    return safe_area_size


def parse(data):
    """ """
    return [tuple(map(int, line.strip().split(","))) for line in data]


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, threshold, expected=None):
    result = solve(parse(read_file(filename)), threshold)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 32, 16)
    main("input.txt", 10000)
