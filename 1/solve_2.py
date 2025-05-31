#!/usr/bin/env python3

from itertools import cycle


def solve(offsets):
    """ """
    frequency = 0
    frequencies = set()
    offsets = cycle(offsets)

    while frequency not in frequencies:
        frequencies.add(frequency)
        frequency += next(offsets)

    return frequency


def parse(data):
    """ """
    return [int(line.strip()) for line in data]


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("input.txt")
