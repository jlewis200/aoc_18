#!/usr/bin/env python3

import re
from dataclasses import dataclass
from collections import defaultdict
import pandas as pd


@dataclass
class Claim:
    claim_id: int
    x: int
    y: int
    height: int
    width: int


def solve(data):
    """
    Find the number of claims to each coordinate, then find the claim containing
    coordinates with only 1 claim.
    """
    claim_counts = defaultdict(lambda: 0)

    for claim in data:
        for x in range(claim.x, claim.x + claim.width):
            for y in range(claim.y, claim.y + claim.height):
                claim_counts[(x, y)] += 1

    for claim in data:
        max_claim_count = 0

        for x in range(claim.x, claim.x + claim.width):
            for y in range(claim.y, claim.y + claim.height):
                max_claim_count = max(max_claim_count, claim_counts[(x, y)])

        if max_claim_count == 1:
            return claim.claim_id

    return None


def parse(data):
    """ """
    claims = []

    for line in data:
        pattern = r"#(?P<claim_id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<width>\d+)x(?P<height>\d+)"
        match = re.fullmatch(pattern, line.strip())
        claims.append(
            Claim(
                claim_id=int(match.group("claim_id")),
                x=int(match.group("x")),
                y=int(match.group("y")),
                width=int(match.group("width")),
                height=int(match.group("height")),
            )
        )

    return claims


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 3)
    main("input.txt")
