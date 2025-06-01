#!/usr/bin/env python3

import re
from dataclasses import dataclass
from collections import defaultdict
import pandas as pd
from itertools import pairwise


def solve(data):
    """ """
    dependencies = init_dependencies(data)
    topological_sort = []
    ready = get_ready(dependencies)

    while len(ready) > 0:
        next_task = sorted(ready)[0]
        del dependencies[next_task]
        topological_sort.append(next_task)
        remove_task(dependencies, next_task)
        ready = get_ready(dependencies)

    return "".join(topological_sort)


def init_dependencies(data):
    dependencies = {}

    for src, dst in data:
        dependencies[dst] = []
        dependencies[src] = []

    for src, dst in data:
        dependencies[dst].append(src)

    return dependencies


def remove_task(dependencies, next_task):
    for src, deps in dependencies.items():
        try:
            deps.remove(next_task)
        except ValueError:
            pass


def get_ready(dependencies):
    ready = set()

    for src, deps in dependencies.items():
        if len(deps) == 0:
            ready.add(src)

    return ready


def parse(data):
    """ """
    edges = []

    for line in data:
        pattern = r"Step (?P<src>.) must be finished before step (?P<dst>.) can begin."
        match = re.fullmatch(pattern, line.strip())
        edges.append((match.group("src"), match.group("dst")))

    return edges


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", "CABDFE")
    main("input.txt")
