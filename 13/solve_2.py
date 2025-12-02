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
        self.crashed = False
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

            collision(carts)

        if terminated(carts) is not None:
            return tuple(terminated(carts)[::-1])

        carts = [cart for cart in carts if not cart.crashed]
        grid_ = grid.copy()

        for cart in sorted(carts):
            grid_[*cart.position] = "#"

    return collision(carts)


def board_str(board):
    """
    Return the string representation of a numpy array where each element can be
    represented as a single character.
    """
    return "\n".join("".join(row) for row in board)


def terminated(carts):
    remaining_carts = sum([not cart.crashed for cart in carts])
    if remaining_carts == 1:
        for cart in carts:
            if not cart.crashed:
                return cart.position
    return None


def collision(carts):
    """ """
    positions = [cart.position for cart in carts if not cart.crashed]
    value, count = np.unique(positions, return_counts=True, axis=0)

    collision_positions = value[count > 1]
    collision_positions = {tuple(pos) for pos in collision_positions}

    if len(collision_positions):
        for cart in carts:
            if tuple(cart.position) in collision_positions:
                cart.crashed = True

                # if (cart.position == np.array([2, 2])).all():
                #    breakpoint()


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
    main("test_1.txt", (6, 4))
    main("input.txt")
