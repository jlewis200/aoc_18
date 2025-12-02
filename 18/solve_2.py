#!/usr/bin/env python3

import itertools
from collections import defaultdict
from aoc_data_structures import VectorTuple
from aoc_data_structures.grid_helpers import grid_str, parse


def solve(grid):
    """
    Run the simulation and maintain a cache of the "forest" grid states.  Once a
    duplicate is detected:
    - calulate the iterations remaining
    - mod by cycle size
    - move forward that number of states in the cycle
    - return value
    """
    string_to_idx = {}
    idx_to_value = {}
    limit = 1000000000

    for idx in range(1, limit + 1):
        grid_copy = grid.copy()

        for y, x in itertools.product(range(grid.shape[0]), range(grid.shape[1])):
            coord = VectorTuple(y, x)
            freqs = get_frequencies(grid, coord)
            grid_copy[coord] = get_next_acre_type(grid, coord, freqs)

        grid = grid_copy
        string = grid_str(grid)
        print(string)
        print()

        if string in string_to_idx:
            remaining_iterations = (limit - idx) % (idx - string_to_idx[string])
            return idx_to_value[string_to_idx[string] + remaining_iterations]

        string_to_idx[string] = idx
        idx_to_value[idx] = (grid == "#").sum() * (grid == "|").sum()

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
    # main("test_0.txt", 1147)
    main("input.txt")
