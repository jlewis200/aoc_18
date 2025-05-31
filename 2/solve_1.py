#!/usr/bin/env python3

import pandas as pd


def solve(data):
    """ """
    double_count = 0
    triple_count = 0

    for box_id in data:
        double_count += is_double(box_id)
        triple_count += is_triple(box_id)

    return double_count * triple_count


def is_double(box_id):
    value_counts = pd.Series(list(box_id)).value_counts()
    return 2 in value_counts.tolist()


def is_triple(box_id):
    value_counts = pd.Series(list(box_id)).value_counts()
    return 3 in value_counts.tolist()


def parse(data):
    """ """
    return list(map(str.strip, data))


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
