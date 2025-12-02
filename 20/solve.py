#!/usr/bin/env python3

import re
import math
import itertools
import numpy as np
import networkx as nx
from aoc_data_structures import VectorTuple

WEST = VectorTuple(0, -1)
EAST = VectorTuple(0, 1)
NORTH = VectorTuple(-1, 0)
SOUTH = VectorTuple(1, 0)


def solve(directions):
    directions = directions[0]

    graph = nx.Graph()
    position = VectorTuple(0, 0)

    dfs(graph, position, directions)
    return max(nx.shortest_path_length(graph, VectorTuple(0, 0)).values())


def dfs(graph, position, directions):
    for idx, direction in enumerate(directions):
        if isinstance(direction, str):
            next_position = position + get_direction(direction)
            graph.add_edge(position, next_position)
            position = next_position

        elif isinstance(direction, list):
            old_position = position

            for branch in direction:
                position = dfs(graph, old_position, branch)

    return position


def graph_str(graph):
    for node in graph.nodes:
        pass


def parse(data):
    data = list(data)[1:-1]
    data = _parse(data)
    return data


def _parse(data):
    directions = [[]]

    while len(data) > 0:
        char = data.pop(0)

        if char in "NESW":
            directions[-1].append(char)

        if char == "(":
            jdx = get_matching_parenthesis(data)
            directions[-1].append(_parse(data[:jdx]))
            data = data[jdx + 1 :]

        elif char == ")":
            breakpoint()

        elif char == "|":
            directions.append([])

    return directions


def get_matching_parenthesis(data):
    level = 1

    for idx, char in enumerate(data):
        if char == "(":
            level += 1

        elif char == ")":
            level -= 1

        if level == 0:
            return idx


def get_direction(direction):
    direction_map = {
        "E": EAST,
        "W": WEST,
        "N": NORTH,
        "S": SOUTH,
    }
    return direction_map[direction]


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 3)
    main("test_1.txt", 10)
    main("test_2.txt", 18)
    main("input.txt")
