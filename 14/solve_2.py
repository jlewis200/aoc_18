#!/usr/bin/env python3


def solve(target):
    elf_0_idx = 0
    elf_1_idx = 1
    recipies = [3, 7]
    recipies_str = ""

    loops = 0

    while target not in recipies_str:
        print(loops)
        loops += 1

        for _ in range(100000):
            new_recipies = recipies[elf_0_idx] + recipies[elf_1_idx]
            new_recipies = str(new_recipies)
            recipies.extend(list(map(int, new_recipies)))

            elf_0_idx += 1 + recipies[elf_0_idx]
            elf_1_idx += 1 + recipies[elf_1_idx]

            elf_0_idx %= len(recipies)
            elf_1_idx %= len(recipies)

        recipies_str = recipies_to_str(recipies)

    return recipies_str.index(target)


def recipies_to_str(recipies):
    return "".join(map(str, recipies))


def main(n_recipies, expected=None):
    result = solve(n_recipies)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("51589", 9)
    main("01245", 5)
    main("92510", 18)
    main("59414", 2018)
    main("74501")
    main("074501")
