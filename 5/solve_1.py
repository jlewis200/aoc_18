#!/usr/bin/env python3

import re
from dataclasses import dataclass
from collections import defaultdict
import pandas as pd
from itertools import pairwise


def solve(data):
    """ """

    while True:
        reduced = reduce(data)

        if len(reduced) == len(data):
            break

        data = reduced

    return len(data)


def reduce(data):
    for idx, (chr_0, chr_1) in enumerate(pairwise(data)):
        if chr_0.lower() == chr_1.lower() and chr_0 != chr_1:
            return data[:idx] + data[idx + 2 :]

    return data


def parse(data):
    """ """
    return data.strip()


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 10)
    main("input.txt")
