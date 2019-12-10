import functools


def opcode(nargs):
    def decorator_opcode(func):
        @functools.wraps(func)
        def wrapper_opcode(*args, **kwargs):
            value = func(*args, **kwargs)
            self = args[0]
            self.cursor += nargs + 1
            return value
        return wrapper_opcode
    return decorator_opcode


class IntCodeComputer:
    def __init__(self, instructions):
        self.instructions = self.parse_instructions(instructions)
        self.opcodes = {1: self.add,
                        2: self.multiply,
                        99: self.halt}
        self.finished = False
        self.cursor = 0

    @staticmethod
    def parse_instructions(instructions):
        return [int(v) for v in instructions.split(',')]

    def execute(self):
        self.finished = False
        self.cursor = 0
        while not self.finished:
            opcode_, modes = self.get_opcode()
            opcode_(modes)

    def get_opcode(self):
        return self.opcodes[self.instructions[self.cursor]], None

    def get(self, index):
        return self.instructions[self.instructions[index]]

    def set(self, index, value):
        self.instructions[self.instructions[index]] = value

    @opcode(3)
    def add(self, _):
        self.set(self.cursor + 3, self.get(self.cursor + 1) + self.get(self.cursor + 2))

    @opcode(3)
    def multiply(self, _):
        self.set(self.cursor + 3, self.get(self.cursor + 1) * self.get(self.cursor + 2))

    def halt(self, _):
        self.finished = True


def main():
    with open('input.txt') as f:
        instructions = f.readline()

    comp = IntCodeComputer(instructions)
    comp.instructions[1] = 12
    comp.instructions[2] = 2
    comp.execute()
    print(f'Value at 0 is {comp.instructions[0]}')

    found = False
    for noun in range(100):
        for verb in range(100):
            comp = IntCodeComputer(instructions)
            comp.instructions[1] = noun
            comp.instructions[2] = verb
            comp.execute()
            if comp.instructions[0] == 19690720:
                found = True
                print(f'Noun is {noun}, verb is {verb},')
                print(f'Checksum is {noun * 100 + verb}')

    if not found:
        print('Not found')


if __name__ == '__main__':
    main()
