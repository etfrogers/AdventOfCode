import re
from collections import defaultdict

instr_re = re.compile('([a-z]*) (inc|dec) (-?[0-9]+) if ([a-z]*) ([<>=!]{1,2}) (-?[0-9]+)')


class Instruction:
    def __init__(self, act_on, op, op_val, cond_reg, cond, cond_val):
        self.act_on = act_on
        self.operation = op
        self.operation_value = int(op_val)
        self.condition_register = cond_reg
        self.condition = cond
        self.condition_value = int(cond_val)

    def __str__(self):
        return ' '.join([str(val) for val in self.__dict__.values()])


class Memory:
    cond_dict = {'==': int.__eq__,
                 '>=': int.__ge__,
                 '<=': int.__le__,
                 '>':  int.__gt__,
                 '<':  int.__lt__,
                 '!=': int.__ne__,
                 }

    def __init__(self):
        self._registers = defaultdict(lambda: 0)
        self.op_dict = {'inc': self.inc, 'dec': self.dec}

    def get(self, name):
        return self._registers[name]

    def set(self, name, value):
        self._registers[name] = value
        return None

    def inc(self, name, value):
        self._registers[name] += value

    def dec(self, name, value):
        self._registers[name] -= value

    def __str__(self):
        return str(self._registers)

    def apply_instruction(self, instr):
        op_func = self.op_dict[instr.operation]
        cond_func = self.cond_dict[instr.condition]

        if cond_func(self.get(instr.condition_register), instr.condition_value):
            op_func(instr.act_on, instr.operation_value)

    def max_value(self):
        return max(self._registers.values())


def parse_instruction(instr):
    matches = instr_re.search(instr)

    # matches[0] is full match
    # assert matches[0] == instr

    return Instruction(*matches.groups())


def build_memory(instructions):
    instructions = [parse_instruction(instr) for instr in instructions]
    #print([str(instr) for instr in instructions])
    bank = Memory()
    for instr in instructions:
        bank.apply_instruction(instr)
    print(bank)
    return bank.max_value()


def main():
    with open('input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    #print(instructions)
    max_val = build_memory(instructions)
    print(max_val)

if __name__ == '__main__':
    main()
