#!/usr/bin/env python3

import re
import math
import itertools
import numpy as np
import networkx as nx

import sys
from aoc_data_structures import VectorTuple
from aoc_data_structures.grid_helpers import grid_str

sys.setrecursionlimit(20000)


def solve(depth, target):
    """
    The prompt states traversal outside the (x, y) bounds of the target is
    possible, but we can't be sure exactly how far.  To use this with networkx
    approach we need concrete bounds.  The board size is doubled, tripled,
    quadrupled, etc. until the minimum path length stops decreasing.  This is a
    heuristic and isn't guaranteed success, but it does work in this case.
    """
    multiplier = 2
    min_path_length = 2**64

    while _solve(depth, target, multiplier) < min_path_length:
        min_path_length = _solve(depth, target, multiplier)
        multiplier += 1

    return min_path_length


def _solve(depth, target, multiplier):
    model = Model(depth, target)
    grid = model.get_grid(target * VectorTuple(multiplier, multiplier))
    graph = get_graph(grid)

    return nx.shortest_path_length(
        graph,
        (0, 0, "torch"),
        (*target, "torch"),
        weight="weight",
    )


def get_graph(grid):
    graph = nx.Graph()

    for y, x in itertools.product(range(grid.shape[0]), range(grid.shape[1])):
        coord = VectorTuple(y, x)

        coord_climb = (*coord, "climb")  # plane:  climbing gear
        coord_torch = (*coord, "torch")  # plane:  torch
        coord_none = (*coord, "none")  # plane:  none

        if grid[coord] == ".":
            graph.add_edge(coord_climb, coord_torch, weight=7)

        elif grid[coord] == "=":
            graph.add_edge(coord_climb, coord_none, weight=7)

        elif grid[coord] == "|":
            graph.add_edge(coord_torch, coord_none, weight=7)

        for adjacency in coord.orthogonals(grid):
            adjacency_climb = (*adjacency, "climb")
            adjacency_torch = (*adjacency, "torch")
            adjacency_none = (*adjacency, "none")

            symbol_set = {grid[coord], grid[adjacency]}

            if symbol_set <= {".", "="}:
                graph.add_edge(coord_climb, adjacency_climb, weight=1)

            if symbol_set <= {".", "|"}:
                graph.add_edge(coord_torch, adjacency_torch, weight=1)

            if symbol_set <= {"|", "="}:
                graph.add_edge(coord_none, adjacency_none, weight=1)
    return graph


class Model:

    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.geologic_index_cache = {}
        self.erosion_level_cache = {}

        self.get_erosion_level(target)
        # self.get_erosion_level(target + VectorTuple(0, -1))
        # self.get_erosion_level(target + VectorTuple(-1, 0))

    def get_geologic_index(self, coord):
        try:
            return self.geologic_index_cache[coord]
        except KeyError:
            self.geologic_index_cache[coord] = self._get_geologic_index(coord)
        return self.geologic_index_cache[coord]

    def _get_geologic_index(self, coord):
        if coord in (VectorTuple(0, 0), self.target):
            return 0

        if coord[0] == 0:
            return coord[1] * 16807

        if coord[1] == 0:
            return coord[0] * 48271

        erosion_level_0 = self.get_erosion_level(coord + VectorTuple(0, -1))
        erosion_level_1 = self.get_erosion_level(coord + VectorTuple(-1, 0))
        return erosion_level_0 * erosion_level_1

    def get_erosion_level(self, coord):
        try:
            return self.erosion_level_cache[coord]
        except KeyError:
            self.erosion_level_cache[coord] = self._get_erosion_level(coord)
        return self.erosion_level_cache[coord]

    def _get_erosion_level(self, coord):
        geologic_index = self.get_geologic_index(coord)
        return (geologic_index + self.depth) % 20183

    def get_grid(self, upper_bound):
        grid = np.full(upper_bound, "X")

        for y in range(upper_bound[0]):
            for x in range(upper_bound[1]):
                coord = VectorTuple(y, x)
                grid[coord] = self.get_terrain(coord)

        return grid

    def get_terrain(self, coord):
        match self.get_erosion_level(coord) % 3:
            case 0:
                return "."
            case 1:
                return "="
            case 2:
                return "|"


def parse(lines):
    depth = re.match(r"depth:\s+(?P<depth>\d+)", lines.pop(0)).group("depth")
    matches = re.match(r"target:\s+(?P<x>\d+),(?P<y>\d+)", lines.pop(0))
    x = matches.group("x")
    y = matches.group("y")

    return int(depth), VectorTuple(int(y), int(x))


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 45)
    main("input.txt")
