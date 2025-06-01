#!/usr/bin/env python3

import re
import numpy as np


def solve(positions, velocities):
    """ """
    positions = np.array(positions)
    velocities = np.array(velocities)

    steps = get_min_spread_steps(positions, velocities)
    positions = positions + (steps * velocities)

    board = np.full((1 + positions.max(),) * 2, ".")
    for position in positions:
        board[*position] = "#"

    print(board_str(board.T))
    print(steps)


def get_min_spread_steps(positions, velocities):
    spread = 2**64

    for idx in range(100000):
        prev_spread = spread
        spread = get_spread(positions)

        if spread > prev_spread:
            break

        positions = positions + velocities

    return idx - 1


def board_str(board):
    """
    Return the string representation of a numpy array where each element can be
    represented as a single character.
    """
    return "\n".join("".join(row) for row in board)


def get_spread(positions):
    """
    Euclidean distance mean from center.
    """
    center = positions.mean(axis=0)
    distances = abs(center - positions)
    return ((distances**2).sum(axis=1) ** 0.5).mean()


def convert_to_tuple(item):
    return tuple(map(lambda x: int(x.strip()), item.split(",")))


def parse(data):
    """ """
    positions = []
    velocities = []

    for line in data:
        pattern = r"position=<(?P<position>.+)> velocity=<(?P<velocity>.+)>"
        match = re.fullmatch(pattern, line.strip())
        positions.append(convert_to_tuple(match.group("position")))
        velocities.append(convert_to_tuple(match.group("velocity")))

    return positions, velocities


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt")
    main("input.txt")
