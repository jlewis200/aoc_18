#!/usr/bin/env python3

from dataclasses import dataclass
from collections import deque


@dataclass
class Node:
    children: list
    metadata: list
    value: int = None

    def get_value(self):
        if self.value is None:
            self.value = self._get_value()

        return self.value

    def _get_value(self):
        if len(self.children) == 0:
            return sum(self.metadata)

        metadata = self.metadata.copy()

        try:
            metadata.remove(0)

        except ValueError:
            pass

        value = 0

        for child_index in metadata:
            child_index -= 1

            try:
                value += self.children[child_index].get_value()

            except IndexError:
                pass

        return value


def solve(data):
    """ """
    tree = extract(data)
    return tree.get_value()


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
    main("test_0.txt", 66)
    main("input.txt")
