import os
import sys
from collections import defaultdict
from AOC2017.day18 import day18


class CoProc(day18.SoundCard):
    def __init__(self, instruction_list):
        self.mul_count = 0
        self.instruction_dict = {'set': self.set,
                                 'sub': self.subtract,
                                 'mul': self.multiply,
                                 'jnz': self.jump_nz,
                                 }
        self.registers = defaultdict(lambda: 0)
        self.instructions = [self.parse_instruction(i) for i in instruction_list]
        self.finished = False
        self.pointer = 0
        self.jumped = False

    def subtract(self, register, value):
        self.registers[register] -= self.get_value(value)

    def multiply(self, register, value):
        self.mul_count += 1
        super().multiply(register, value)

    def jump_nz(self, register, value):
        if self.get_value(register) != 0:
            self.pointer += self.get_value(value)
            self.jumped = True


def main():
    with open('input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    print(instructions)
    coproc = CoProc(instructions)
    coproc.execute()
    print(coproc.mul_count)


if __name__ == '__main__':
    main()
