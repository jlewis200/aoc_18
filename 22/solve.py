#!/usr/bin/env python3

import re
import math
import itertools
import numpy as np
import networkx as nx

import sys
from aoc_data_structures import VectorTuple

sys.setrecursionlimit(10000)


def solve(depth, target):
    model = Model(depth, target)
    model.get_erosion_level(target)
    model.get_erosion_level(target + VectorTuple(0, -1))
    model.get_erosion_level(target + VectorTuple(-1, 0))
    return sum(list(map(lambda x: x % 3, model.erosion_level_cache.values())))


class Model:

    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.geologic_index_cache = {}
        self.erosion_level_cache = {}
        #self.init_erosion_levels()

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

    def init_erosion_levels(self):
        for y, x in itertools.product(range(self.target[0]), range(self.target[0])):
            coord = VectorTuple(y, x)
            self.get_erosion_level(coord)

    def get_erosion_level(self, coord):
        try:
            return self.erosion_level_cache[coord]
        except KeyError:
            self.erosion_level_cache[coord] = self._get_erosion_level(coord)
        return self.erosion_level_cache[coord]

    def _get_erosion_level(self, coord):
        geologic_index = self.get_geologic_index(coord)
        return (geologic_index + self.depth) % 20183


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
    main("test_0.txt", 114)
    main("input.txt")
