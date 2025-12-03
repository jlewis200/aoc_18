#!/usr/bin/env python3

from dataclasses import dataclass
from collections import deque
import numpy as np
import networkx as nx


@dataclass
class Unit:
    position: tuple
    variety: str
    attack_power: int = 3
    hit_points: int = 200

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __hash__(self):
        return (self.position[0] * 1000) + self.position[1]

    def move(self, units):
        if self.variety == "#":
            return

        candidates = self.get_movement_candidates(units)

        if len(candidates) in (0, 1):
            return

        self.position = candidates[1]

    def build_graph(self, units):
        grid = self.build_grid(units)
        grid[self.position] = "."
        edges = []

        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):

                if grid[(y, x)] != ".":
                    continue

                for other in [
                    (y + 1, x),
                    (y - 1, x),
                    (y, x + 1),
                    (y, x - 1),
                ]:
                    if grid[other] == ".":
                        edges.append((other, (y, x)))

        return nx.Graph(edges)

    def build_grid(self, units):
        ys = []
        xs = []

        for unit in units:
            ys.append(unit.position[0])
            xs.append(unit.position[1])

        grid = np.full((1 + max(ys), 1 + max(xs)), ".")

        for unit in units:
            grid[unit.position] = unit.variety

        return grid

    def get_path(self, target, graph):
        try:
            paths = list(nx.all_shortest_paths(graph, self.position, target))
        except nx.exception.NodeNotFound:
            return []

        if len(paths) == 0:
            return []

        if len(paths) == 1:
            return paths[0]

        first_steps = []

        for path in paths:
            first_steps.append(Unit(position=path[1], variety=""))

        idx = np.argmin(first_steps)

        return paths[idx]

    def get_movement_candidates(self, units):
        grid = self.build_grid(units)
        graph = self.build_graph(units)

        grid[self.position] = "."

        target = "E" if self.variety == "G" else "G"
        queue = deque([self.position])
        pending = set()

        while len(queue) > 0:
            position = queue.popleft()

            if grid[position] != ".":
                continue

            y, x = position

            for adjacency in [
                (y - 1, x),
                (y, x - 1),
                (y, x + 1),
                (y + 1, x),
            ]:
                if grid[adjacency] == target:
                    return self.get_path(position, graph)

                if adjacency not in pending:
                    queue.append(adjacency)
                    pending.add(adjacency)

        return []

    def attack(self, units):
        if self.variety not in ("E", "G"):
            return

        targets = []
        y, x = self.position
        adjacencies = [
            (y + 1, x),
            (y - 1, x),
            (y, x + 1),
            (y, x - 1),
        ]

        min_hp = 2**32

        for unit in units:
            if unit.variety in (self.variety, "#"):
                continue

            if unit.position in adjacencies:
                targets.append(unit)
                min_hp = min(unit.hit_points, min_hp)

        if len(targets) > 0:
            targets = sorted(targets)

            for target in targets:
                if target.hit_points == min_hp:

                    target.hit_points -= self.attack_power
                    if target.hit_points <= 0:
                        units.remove(target)

                    break


def solve(data):
    for elf_power in range(100):
        result = solve_(data, elf_power)

        if result is not None:
            return result


def count_elves(units):
    n_elves = 0

    for unit in units:
        if unit.variety == "E":
            n_elves += 1

    return n_elves


def solve_(data, elf_power=3):
    grid = np.array(data)
    units = get_units(grid, elf_power)
    iteration = 0

    animate(units)
    n_elves = count_elves(units)

    while not is_complete(units):
        iteration += 1

        for unit in sorted(units):
            if unit not in units:
                continue

            if unit.variety not in ("E", "G"):
                continue

            if is_complete(units):
                iteration -= 1
                break

            unit.move(units)
            unit.attack(units)

        if n_elves != count_elves(units):
            return None

    animate(units)

    hit_points = sum(unit.hit_points for unit in units if unit.hit_points > 0)
    print(iteration, hit_points)
    return iteration * hit_points


def animate(units):
    grid = units[0].build_grid(units)
    print(board_str(grid))
    print()


def board_str(board):
    """
    Return the string representation of a numpy array where each element can be
    represented as a single character.
    """
    return "\n".join("".join(row) for row in board)


def is_complete(units):
    unit_varieties = set()

    for unit in units:
        unit_varieties.add(unit.variety)

    return len(unit_varieties) == 2


def get_walls(grid):
    walls = []

    for wall in list(map(tuple, np.argwhere(grid == "#"))):
        wall = tuple(map(int, wall))
        wall = Unit(position=wall, variety="#", attack_power=0, hit_points=0)
        walls.append(wall)

    return walls


def get_goblins(grid):
    goblins = []

    for goblin in list(map(tuple, np.argwhere(grid == "G"))):
        goblin = tuple(map(int, goblin))
        goblin = Unit(position=goblin, variety="G")
        goblins.append(goblin)

    return goblins


def get_elves(grid, elf_power):
    elves = []

    for elf in list(map(tuple, np.argwhere(grid == "E"))):
        elf = tuple(map(int, elf))
        elf = Unit(position=elf, variety="E", attack_power=elf_power)
        elves.append(elf)

    return elves


def get_units(grid, elf_power):
    units = []
    units.extend(get_goblins(grid))
    units.extend(get_elves(grid, elf_power))
    units.extend(get_walls(grid))

    return units


def parse(data):
    return [list(line.strip()) for line in data]


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 4988)
    # main("test_1.txt", 36334)
    main("test_2.txt", 31284)
    main("test_3.txt", 3478)
    main("test_4.txt", 6474)
    main("test_5.txt", 1140)
    main("input.txt")
