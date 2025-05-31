#!/usr/bin/env python3

import re
from dataclasses import dataclass
from collections import defaultdict
import pandas as pd
from itertools import pairwise
from string import ascii_lowercase


def solve(data):
    """ """

    min_length = 2**32

    for char in ascii_lowercase:
        data_ = discard(data, char)
        length = reduced_length(data_)
        min_length = min(length, min_length)
        print(min_length)

    return min_length


def discard(data, discard_char):
    data = list(data)
    filtered = []

    for char in data:
        if char not in (discard_char.lower(), discard_char.upper()):
            filtered.append(char)

    return "".join(filtered)


def reduced_length(data):
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
    main("test_0.txt", 4)
    main("input.txt")
