#!/usr/bin/env python3

import re
from dataclasses import dataclass
from collections import defaultdict
import pandas as pd
from itertools import pairwise
import numpy as np
import json


@dataclass
class Instruction:
    opcode: int
    input_0: int
    input_1: int
    output: int


@dataclass
class Sample:
    before: list[int]
    after: list[int]
    instruction: Instruction


class Interpreter:

    def __init__(self, registers=None):
        self.registers = [0, 0, 0, 0] if registers is None else registers.copy()
        self.opcode_map = {
            0: self.addr,
            1: self.addi,
            2: self.mulr,
            3: self.muli,
            4: self.banr,
            5: self.bani,
            6: self.borr,
            7: self.bori,
            8: self.setr,
            9: self.seti,
            10: self.gtir,
            11: self.gtri,
            12: self.gtrr,
            13: self.eqir,
            14: self.eqri,
            15: self.eqrr,
        }

    def perform_instruction(self, instruction):
        # map integers to functions
        pass

    def addr(self, instruction):
        self.registers[instruction.output] = (
            self.registers[instruction.input_0] + self.registers[instruction.input_1]
        )

    def addi(self, instruction):
        self.registers[instruction.output] = (
            self.registers[instruction.input_0] + instruction.input_1
        )

    def mulr(self, instruction):
        self.registers[instruction.output] = (
            self.registers[instruction.input_0] * self.registers[instruction.input_1]
        )

    def muli(self, instruction):
        self.registers[instruction.output] = (
            self.registers[instruction.input_0] * instruction.input_1
        )

    def banr(self, instruction):
        self.registers[instruction.output] = (
            self.registers[instruction.input_0] & self.registers[instruction.input_1]
        )

    def bani(self, instruction):
        self.registers[instruction.output] = (
            self.registers[instruction.input_0] & instruction.input_1
        )

    def borr(self, instruction):
        self.registers[instruction.output] = (
            self.registers[instruction.input_0] | self.registers[instruction.input_1]
        )

    def bori(self, instruction):
        self.registers[instruction.output] = (
            self.registers[instruction.input_0] | instruction.input_1
        )

    def setr(self, instruction):
        self.registers[instruction.output] = self.registers[instruction.input_0]

    def seti(self, instruction):
        self.registers[instruction.output] = instruction.input_0

    def gtir(self, instruction):
        self.registers[instruction.output] = (
            instruction.input_0 > self.registers[instruction.input_1]
        )

    def gtri(self, instruction):
        self.registers[instruction.output] = (
            self.registers[instruction.input_0] > instruction.input_1
        )

    def gtrr(self, instruction):
        self.registers[instruction.output] = (
            self.registers[instruction.input_0] > self.registers[instruction.input_1]
        )

    def eqir(self, instruction):
        self.registers[instruction.output] = (
            instruction.input_0 == self.registers[instruction.input_1]
        )

    def eqri(self, instruction):
        self.registers[instruction.output] = (
            self.registers[instruction.input_0] == instruction.input_1
        )

    def eqrr(self, instruction):
        self.registers[instruction.output] = (
            self.registers[instruction.input_0] == self.registers[instruction.input_1]
        )


def solve(samples, program):
    """ """
    three_or_more_opcodes = 0

    for sample in samples:
        consistent_count = 0

        for opcode in range(16):
            interpreter = Interpreter(sample.before)
            interpreter.opcode_map[opcode](sample.instruction)
            consistent_count += interpreter.registers == sample.after

        three_or_more_opcodes += consistent_count >= 3

    return three_or_more_opcodes


def parse(data):
    """ """
    samples_data, program = data.split("\n\n\n\n")
    samples_data = samples_data.split("\n\n")

    samples = []

    for sample in samples_data:
        before, instruction, after = sample.split("\n")

        before = json.loads(before[8:])
        before = list(map(int, before))

        after = json.loads(after[8:])
        after = list(map(int, after))

        instruction = Instruction(*map(int, instruction.split()))
        sample = Sample(before, after, instruction)
        samples.append(sample)

    return samples, program


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("input.txt")
