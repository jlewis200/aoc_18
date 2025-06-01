#!/usr/bin/env python3

import re
from dataclasses import dataclass
from collections import defaultdict
import pandas as pd
from itertools import pairwise


def solve(data, n_workers, base_time):
    """ """
    dependencies = init_dependencies(data)
    topological_sort = []
    ready = get_ready(dependencies)
    timer = {}
    n_seconds = 0

    while len(ready) > 0 or len(timer) > 0:

        # fill timer
        while len(ready) > 0 and len(timer) < n_workers:
            next_task = sorted(ready)[0]
            timer[next_task] = base_time + 1 + (ord(next_task) - ord("A"))
            del dependencies[next_task]
            ready = get_ready(dependencies)

        # complete the shortest duration task(s)
        min_task_time = min(timer.values())

        for task in list(timer.keys()):
            timer[task] -= min_task_time

            if timer[task] == 0:
                del timer[task]
                remove_task(dependencies, task)
                topological_sort.append(task)

        n_seconds += min_task_time
        ready = get_ready(dependencies)

    return n_seconds


def get_min_task_time(timer):
    min_task_time = 2**32

    for task, time in timer.items():
        if time < min_task_time:
            min_task_time = time
            min_task = task

    return min_task_time


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


def main(filename, *args, expected=None):
    result = solve(parse(read_file(filename)), *args)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 2, 0, expected=15)
    main("input.txt", 5, 60)
