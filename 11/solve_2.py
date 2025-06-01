#!/usr/bin/env python3

import numpy as np


def solve(serial_number):
    """ """
    grid = np.zeros((301, 301), dtype=int)

    for x in range(1, 301):
        for y in range(1, 301):
            grid[y, x] = get_power(x, y, serial_number)

    max_cell_power = -(2**32)

    for size in range(1, 20):
        cell_power, cell = get_max_cell(grid, size)

        if cell_power > max_cell_power:
            max_cell = cell + (size,)
            max_cell_power = cell_power

    return max_cell


def get_max_cell(grid, size):
    max_cell_power = -(2**32)

    for x in range(1, 301 - size):
        for y in range(1, 301 - size):
            cell_power = grid[y : y + size, x : x + size].sum()

            if cell_power > max_cell_power:
                max_cell = (x, y)
                max_cell_power = cell_power

    return max_cell_power, max_cell


def get_power(x, y, serial_number):
    rack_id = x + 10
    power = rack_id * y
    power += serial_number
    power *= rack_id
    power = (power // 100) % 10
    power -= 5
    return power


def main(serial_number, expected=None):
    result = solve(serial_number)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main(18, (90, 269, 16))
    main(42, (232, 251, 12))
    main(9424)
