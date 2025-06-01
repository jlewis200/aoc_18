#!/usr/bin/env python3

import re
import numpy as np


def solve(initial_state, rules):
    """ """
    generation = initial_state
    print_generation(generation)

    for _ in range(20):
        next_generation = set()

        for idx in range(-200, 200):
            for rule in rules:
                if should_apply(generation, rule, idx):
                    next_generation.add(idx)
                    break

        generation = next_generation
        print_generation(generation)

    return sum(generation)


def should_apply(generation, rule, idx):
    apply = True

    for offset, value in rule.items():

        if value:
            apply &= (idx + offset) in generation

        else:
            apply &= (idx + offset) not in generation

    return apply


def print_generation(generation):
    string = ""

    for idx in range(-200, 1 + max(generation)):
        if idx in generation:
            string += "#"
        else:
            string += "."

    print(string)


def parse(data):
    """ """
    line = data.pop(0).strip()
    line = line.removeprefix("initial state: ")
    initial_state = set()

    for idx, pot in enumerate(line):
        if pot == "#":
            initial_state.add(idx)

    data.pop(0)
    rules = []

    for line in data:
        pattern = r"(?P<state>.+) => (?P<outcome>.+)"
        match = re.fullmatch(pattern, line.strip())

        if match.group("outcome") == "#":
            rule = dict(
                zip([-2, -1, 0, 1, 2], np.array(list(match.group("state"))) == "#")
            )
            rules.append(rule)

    return initial_state, rules


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 325)
    main("input.txt")
