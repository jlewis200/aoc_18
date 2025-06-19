#!/usr/bin/env python3

import re
from dataclasses import dataclass
from collections import defaultdict
import pandas as pd
from itertools import pairwise


def solve(n_recipies):
    """ """
    elf_0_idx = 0
    elf_1_idx = 1
    recipies = [3, 7]

    while len(recipies) < (n_recipies + 10):
        new_recipies = recipies[elf_0_idx] + recipies[elf_1_idx]
        new_recipies = str(new_recipies)
        recipies.extend(list(map(int, new_recipies)))

        elf_0_idx += 1 + recipies[elf_0_idx]
        elf_1_idx += 1 + recipies[elf_1_idx]

        elf_0_idx %= len(recipies)
        elf_1_idx %= len(recipies)

    return "".join(map(str, recipies[n_recipies : n_recipies + 10]))


def main(n_recipies, expected=None):
    result = solve(n_recipies)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main(9, "5158916779")
    main(5, "0124515891")
    main(18, "9251071085")
    main(2018, "5941429882")
    main(74501)
