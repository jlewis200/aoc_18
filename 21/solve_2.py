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
    opcode: str
    input_0: int
    input_1: int
    output: int


@dataclass
class Sample:
    before: list[int]
    after: list[int]
    instruction: Instruction


class Interpreter:

    def __init__(self, ip_register, program, registers=None):
        self.registers = [0, 0, 0, 0, 0, 0] if registers is None else registers.copy()
        self.ip_register = ip_register
        self.program = program
        self.opcode_map = {
            "addr": self.addr,
            "addi": self.addi,
            "mulr": self.mulr,
            "muli": self.muli,
            "banr": self.banr,
            "bani": self.bani,
            "borr": self.borr,
            "bori": self.bori,
            "setr": self.setr,
            "seti": self.seti,
            "gtir": self.gtir,
            "gtri": self.gtri,
            "gtrr": self.gtrr,
            "eqir": self.eqir,
            "eqri": self.eqri,
            "eqrr": self.eqrr,
        }
        self.remapped_opcodes = {}

    def run(self):
        """
        Assume them program generates values to compare to the input (reg_0) in
        a cycle.  Run the program and cache the comparison value of reg_5 at
        instruction 28.  When the first cache duplicate is observed, the
        previous cache value can be assumed to be the "furthest" from the cycle
        start, and it must be the value which would run the most instructions.
        """
        cache = []

        while self.registers[self.ip_register] < len(self.program):
            if self.registers[self.ip_register] == 28:
                reg_5 = self.registers[5]

                if reg_5 in cache:
                    print(cache[-1])
                    return
                
                cache.append(reg_5)

            self.perform_instruction(self.program[self.registers[self.ip_register]])
            self.registers[self.ip_register] += 1

    def perform_instruction(self, instruction):
        self.opcode_map[instruction.opcode](instruction)

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


def solve(ip_register, program):
    """ """
    interpreter = Interpreter(ip_register, program, registers=[-1, 0, 0, 0, 0, 0])
    interpreter.run()
    return interpreter.registers[0]


def parse(lines):
    """ """
    line = lines.pop(0)
    ip_register = int(re.match(r".*(?P<ip_register>\d+).*", line).group("ip_register"))

    program = []

    for line in lines:
        opcode, *args = line.strip().split()
        input_0, input_1, output = list(map(int, args))
        program.append(Instruction(opcode, input_0, input_1, output))

    return ip_register, program


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("input.txt")
