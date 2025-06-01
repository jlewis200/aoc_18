#!/usr/bin/env python3

from dataclasses import dataclass
from collections import deque


@dataclass
class Node:
    children: list
    metadata: list


def solve(data):
    """ """
    tree = extract(data)

    queue = deque([tree])
    metadata_sum = 0

    while len(queue) > 0:
        node = queue.popleft()
        metadata_sum += sum(node.metadata)

        for child in node.children:
            queue.append(child)

    return metadata_sum


def extract(data):
    n_children = data.pop(0)
    n_metadata = data.pop(0)

    children = []
    metadata = []

    for _ in range(n_children):
        children.append(extract(data))

    for _ in range(n_metadata):
        metadata.append(data.pop(0))

    return Node(children, metadata)


def parse(data):
    """ """
    return list(map(int, data.strip().split()))


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 138)
    main("input.txt")
