#!/usr/bin/env python3


def solve(data):
    """ """
    for idx, str_0 in enumerate(data):
        for str_1 in data[idx + 1 :]:
            differ_indices = string_difference(str_0, str_1)
            if len(differ_indices) == 1:
                str_0 = list(str_0)
                str_0.pop(differ_indices[0])
                return "".join(str_0)
    return None


def string_difference(str_0, str_1):
    differ_indices = []

    for idx, (chr_0, chr_1) in enumerate(zip(str_0, str_1)):
        if chr_0 != chr_1:
            differ_indices.append(idx)
        if len(differ_indices) > 1:
            break

    return differ_indices


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
    main("test_1.txt", "fgij")
    main("input.txt")
