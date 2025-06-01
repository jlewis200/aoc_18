#!/usr/bin/env python3

import re
from collections import defaultdict


class Node:

    def __init__(
        self,
        value,
    ):

        self.value = value
        self.left = self
        self.right = self

    def append_right(self, other):
        other.right = self.right
        other.left = self

        self.right.left = other
        self.right = other

    def remove(self):
        self.left.right = self.right
        self.right.left = self.left


def solve(n_players, final_marble_index):
    """ """
    final_marble_index *= 100
    node = Node(0)
    scores = defaultdict(lambda: 0)

    for marble_index in range(1, 1 + final_marble_index):

        if marble_index % 23 == 0:

            for _ in range(7):
                node = node.left

            marble_value = marble_index + node.value
            player_index = marble_index % n_players
            player_index = n_players if player_index == 0 else player_index

            scores[player_index] += marble_value
            node.remove()
            node = node.right

        else:
            new_node = Node(marble_index)
            node.right.append_right(new_node)
            node = new_node

        marble_index += 1

    return max(scores.values())


def parse(data):
    """ """
    pattern = r"(?P<n_players>\d+) players; last marble is worth (?P<final_marble_index>\d+) points"
    match = re.fullmatch(pattern, data.strip())
    return (
        int(match.group("n_players")),
        int(match.group("final_marble_index")),
    )


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("input.txt")
