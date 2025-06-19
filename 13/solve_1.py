#!/usr/bin/env python3

from time import sleep
import numpy as np

R = (0, 1)
U = (-1, 0)
L = (0, -1)
D = (1, 0)


class Cart:

    def __init__(self, position, orientation):
        self.position = position

        self.delta = {">": R, "^": U, "<": L, "v": D}[orientation]
        self.intersection_turn_queue = ["left", "straight", "right"]

    def intersection(self):
        turn = self.intersection_turn_queue.pop(0)
        self.intersection_turn_queue.append(turn)

        if turn == "straight":
            return

        if turn == "left" and self.delta == R:
            self.delta = U

        elif turn == "left" and self.delta == U:
            self.delta = L

        elif turn == "left" and self.delta == L:
            self.delta = D

        elif turn == "left" and self.delta == D:
            self.delta = R

        elif turn == "right" and self.delta == R:
            self.delta = D

        elif turn == "right" and self.delta == U:
            self.delta = R

        elif turn == "right" and self.delta == L:
            self.delta = U

        elif turn == "right" and self.delta == D:
            self.delta = L

    def turn(self, tile):

        if tile == "\\" and self.delta == R:
            self.delta = D

        elif tile == "\\" and self.delta == U:
            self.delta = L

        elif tile == "\\" and self.delta == L:
            self.delta = U

        elif tile == "\\" and self.delta == D:
            self.delta = R

        elif tile == "/" and self.delta == R:
            self.delta = U

        elif tile == "/" and self.delta == U:
            self.delta = R

        elif tile == "/" and self.delta == L:
            self.delta = D

        elif tile == "/" and self.delta == D:
            self.delta = L

    def step(self, grid):
        if grid[*self.position] == "+":
            self.intersection()

        if grid[*self.position] in ("/", "\\"):
            self.turn(grid[*self.position])

        self.position += self.delta

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __hash__(self):
        return int(self.position[0] * 1_000_000 + self.position[1])

    def __repr__(self):
        return f"{self.position}\t{self.delta}"


def solve(grid):
    """ """
    cart_coords = np.argwhere(np.isin(grid, tuple("><v^")))
    carts = [Cart(cart_coord, grid[*cart_coord]) for cart_coord in cart_coords]

    tick = 0
    run = True

    while run:
        tick += 1

        for cart in sorted(carts):
            cart.step(grid)

            if collision(carts) is not None:
                run = False
                break

        grid_ = grid.copy()

        for cart in sorted(carts):
            grid_[*cart.position] = "#"

        sleep(0.1)
        print(board_str(grid_))
        print("#" * 160)

    return collision(carts)


def board_str(board):
    """
    Return the string representation of a numpy array where each element can be
    represented as a single character.
    """
    return "\n".join("".join(row) for row in board)


def collision(carts):
    """
    Return true if collision.
    """
    positions = [cart.position for cart in carts]
    value, count = np.unique(positions, return_counts=True, axis=0)

    if count.max() > 1:
        return tuple(value[count.argmax()])[::-1]

    return None


def parse(data):
    """ """
    grid = []

    for line in data:
        grid.append(list(line.removesuffix("\n")))

    return np.array(grid)


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", (7, 3))
    main("input.txt")
