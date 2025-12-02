#!/usr/bin/env python3

import itertools
from collections import defaultdict
from aoc_data_structures import VectorTuple
from aoc_data_structures.grid_helpers import grid_str, parse


def solve(grid):
    for _ in range(10):
        grid_copy = grid.copy()

        for y, x in itertools.product(range(grid.shape[0]), range(grid.shape[1])):
            coord = VectorTuple(y, x)
            freqs = get_frequencies(grid, coord)
            grid_copy[coord] = get_next_acre_type(grid, coord, freqs)

        grid = grid_copy
        print(grid_str(grid))
        print()

    value = (grid == "#").sum() * (grid == "|").sum()
    return value


def get_frequencies(grid, coord):
    freqs = defaultdict(lambda: 0)

    for adjacency in coord.adjacencies(grid):
        freqs[grid[adjacency]] += 1

    return freqs


def get_next_acre_type(grid, coord, freqs):
    if grid[coord] == ".":
        if freqs["|"] >= 3:
            return "|"
        return "."

    if grid[coord] == "|":
        if freqs["#"] >= 3:
            return "#"
        return "|"

    if grid[coord] == "#":
        if freqs["#"] >= 1 and freqs["|"] >= 1:
            return "#"
        return "."


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 1147)
    main("input.txt")
