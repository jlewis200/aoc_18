#!/usr/bin/env python3

import re
import z3
from aoc_data_structures import VectorTuple


def solve(parsed):
    """
    Steps:
    - create a z3 model
    - use symbolic x, y, z to represent coordinate
    - sum manhattan distance of symbolic coord and each nanobot <= radius
    - sweep constraint that summation > min_threshold until not satisfiable

    The resulting coord has the most overlap of any coord.  It is not
    guaranteed to be the closest.  For a more robust solution additional
    enumeration of maximal coords would be required.  This solution works
    for example data and my test data, but it's not guaranteed to work for
    arbitrary input.
    """
    nanobots = [VectorTuple(*args[:-1]) for args in parsed]
    radii = [args[-1] for args in parsed]
    solver = z3.Solver()

    x, y, z = z3.Ints("x y z")
    summation = 0

    for nanobot, radius in zip(nanobots, radii):
        delta = z3.Abs(x - nanobot[0]) + z3.Abs(y - nanobot[1]) + z3.Abs(z - nanobot[2])
        summation += delta <= radius

    max_in_range = 0
    satisfiable = True

    while satisfiable:
        solver.add(summation > max_in_range)
        satisfiable = str(solver.check()) == "sat"

        if satisfiable:
            vector = VectorTuple(
                solver.model()[x].as_long(),
                solver.model()[y].as_long(),
                solver.model()[z].as_long(),
            )
            max_in_range = get_in_range(vector, nanobots, radii)
            print(f"{max_in_range}\t\t{vector}")

    return vector.manhattan()


def get_in_range(target, nanobots, radii):
    """
    Given a list of nanobots and corresponding radii, determine the number of
    nanobots the target is within range of.
    """
    in_range = 0

    for nanobot, radius in zip(nanobots, radii):
        if manhattan(target, nanobot) <= radius:
            in_range += 1

    return in_range


def manhattan(vt_0, vt_1):
    return sum(abs(vt_0 - vt_1))


def parse(lines):
    parsed = []

    for line in lines:
        match = re.match(r"pos=<(?P<x>.+),(?P<y>.+),(?P<z>.+)>, r=(?P<r>.+)", line)
        x, y, z, r = (
            match.group("x"),
            match.group("y"),
            match.group("z"),
            match.group("r"),
        )
        parsed.append(tuple(map(int, (x, y, z, r))))

    return parsed


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_1.txt", 36)
    main("input.txt")
