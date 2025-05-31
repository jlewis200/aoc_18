#!/usr/bin/env python3


def solve(offsets):
    """ """
    return sum(offsets)


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
