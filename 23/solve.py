#!/usr/bin/env python3

import re
import numpy as np
from aoc_data_structures import VectorTuple


def solve(parsed):
    nanobots = [VectorTuple(*args[:-1]) for args in parsed]
    radii = [args[-1] for args in parsed]
    max_radius_nanobot, max_radius = get_maxes(nanobots, radii)
    in_range = 0

    for nanobot in nanobots:
        if manhattan(max_radius_nanobot, nanobot) <= max_radius:
            in_range += 1

    return in_range


def manhattan(vt_0, vt_1):
    return sum(abs(vt_0 - vt_1))


def get_maxes(nanobots, radii):
    idx = np.argmax(radii)
    max_radius = radii[idx]
    max_radius_nanobot = nanobots[idx]
    return max_radius_nanobot, max_radius


def parse(lines):
    parsed = []

    for line in lines:
        match = re.match(r"pos=<(?P<x>.+),(?P<y>.+),(?P<z>.+)>, r=(?P<r>.+)", line)
        x, y, z, r = (
            match.group("x"),
            match.group("y"),
            match.group("z"),
            match.group("r"),
        )
        parsed.append(tuple(map(int, (x, y, z, r))))

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
    main("test_0.txt", 7)
    main("input.txt")
