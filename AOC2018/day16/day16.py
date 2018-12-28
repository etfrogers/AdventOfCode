import math
import re
from AOC2018.day16 import reddit_day16

PATTERNS = [re.compile(r'Before: \[(\d+), (\d+), (\d+), (\d+)\]'),
            re.compile(r'(\d+) (\d+) (\d+) (\d+)'),
            re.compile(r'After:  \[(\d+), (\d+), (\d+), (\d+)\]')]


class Sample:
    def __init__(self, input_):
        matches = [pat.match(line) for pat, line in zip(PATTERNS, input_)]
        self.before_state = tuple((int(g) for g in matches[0].groups()))
        self.opcode_data = tuple((int(g) for g in matches[1].groups()))
        self.after_state = tuple((int(g) for g in matches[2].groups()))


class Opcode:
    def __init__(self, label, func, derefA, derefB, useB=True):
        self.label = label
        self.func = func
        self.derefA = derefA
        self.derefB = derefB
        self.useB = useB

    def __call__(self, input_state, command, *args, **kwargs):
        output_state = list(input_state)
        if self.derefA:
            a = input_state[command[0]]
        else:
            a = command[0]
        if self.derefB:
            b = input_state[command[1]]
        else:
            b = command[1]
        if self.func is None:
            assert not self.useB
            val = a
        elif self.useB:
            val = self.func(a, b)
        else:
            val = self.func(a)
        output_state[command[2]] = int(val)
        return tuple(output_state)

    def __str__(self):
        return self.label


class Device:
    opcodes = {'addr': Opcode('addr', int.__add__, derefA=True, derefB=True),
               'addi': Opcode('addi', int.__add__, derefA=True, derefB=False),
               'mulr': Opcode('mulr', int.__mul__, derefA=True, derefB=True),
               'muli': Opcode('muli', int.__mul__, derefA=True, derefB=False),
               'banr': Opcode('banr', int.__and__, derefA=True, derefB=True),
               'bani': Opcode('bani', int.__and__, derefA=True, derefB=False),
               'borr': Opcode('borr', int.__or__, derefA=True, derefB=True),
               'bori': Opcode('bori', int.__or__, derefA=True, derefB=False),
               'setr': Opcode('setr', None, derefA=True, derefB=None, useB=False),
               'seti': Opcode('seti', None, derefA=False, derefB=None, useB=False),
               'gtir': Opcode('gtir', int.__gt__, derefA=False, derefB=True),
               'gtri': Opcode('gtri', int.__gt__, derefA=True, derefB=False),
               'gtrr': Opcode('gtrr', int.__gt__, derefA=True, derefB=True),
               'eqir': Opcode('eqir', int.__eq__, derefA=False, derefB=True),
               'eqri': Opcode('eqri', int.__eq__, derefA=True, derefB=False),
               'eqrr': Opcode('eqrr', int.__eq__, derefA=True, derefB=True),
               }
    assert len(opcodes) == 16

    def __init__(self, n_registers=4):
        self.opcode_map = dict()
        self.registers = [0] * n_registers

    def reset(self):
        self.registers = [0] * len(self.registers)

    def working_opcodes(self, sample):
        return set((opcode.label for opcode in self.opcodes.values() if self.opcode_works(opcode, sample)))

    def n_opcodes(self, sample):
        return len(self.working_opcodes(sample))

    @staticmethod
    def opcode_works(opcode, sample):
        return sample.after_state == opcode(sample.before_state, sample.opcode_data[1:])

    def build_opcode_mapping(self, samples):
        while len(self.opcode_map) < len(self.opcodes):
            for sample in samples:
                possibilities = self.working_opcodes(sample)
                possibilities.difference_update(self.opcode_map.values())
                if len(possibilities) == 1:
                    known_code = possibilities.pop()
                    self.opcode_map[sample.opcode_data[0]] = known_code

    def run(self, program):
        self.reset()
        for line in self.parse_program(program):
            self.execute_line(line)

    def execute_line(self, line):
        opcode = line[0]
        data = line[1]
        result = opcode(self.registers, data)
        self.registers = list(result)

    def parse_program(self, program):
        if type(program) is str:
            program = program.split('\n')
        parsed = []
        for line in program:
            opcode_name, *data = line.split()
            data = [int(v) for v in data]
            try:
                opcode_num = int(opcode_name)
                opcode_name = self.opcode_map[opcode_num]
            except ValueError:
                pass
            opcode = self.opcodes[opcode_name]
            parsed.append((opcode, data))
        return parsed


def input_to_samples(input_):
    data = []
    for i in range(math.ceil(len(input_) / 4)):
        data.append(input_[4 * i:4 * i + 3])
    return [Sample(d) for d in data]


def main():
    device = Device()
    with open('input.txt') as f:
        input_ = f.read()
    input_ = input_.split('\n\n\n\n')

    input_part1, input_part2 = ([line.strip() for line in part.split('\n')] for part in input_)
    samples = input_to_samples(input_part1)

    n = sum([1 if device.n_opcodes(sample) >= 3 else 0 for sample in samples ])

    print(n)

    device.build_opcode_mapping(samples)

    device.run(input_part2)

    print(device.registers)


if __name__ == '__main__':
    main()