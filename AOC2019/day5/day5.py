from AOC2019.day2.day2 import IntCodeComputer, opcode


class IntCodeComputer2(IntCodeComputer):
    def __init__(self, instructions, input_=None):
        super().__init__(instructions)
        self.opcodes = {1: self.add,
                        2: self.multiply,
                        99: self.halt,
                        3: self.input,
                        4: self.output,
                        }
        self.input_data = input_
        self.output_data = []

    def get_opcode(self):
        value = self.instructions[self.cursor]
        str_ = '{:05d}'.format(value)
        modes = str_[:-2]
        code = int(str_[-2:])
        modes = tuple(reversed([int(c) for c in modes]))
        return self.opcodes[code], modes

    # noinspection PyMethodOverriding
    def get(self, index, mode):
        if mode == 0:
            return self.instructions[self.instructions[index]]
        elif mode == 1:
            return self.instructions[index]
        else:
            raise ValueError

    # noinspection PyMethodOverriding
    def set(self, index, value, mode):
        if mode == 0:
            self.instructions[self.instructions[index]] = value
        elif mode == 1:
            self.instructions[index] = value
        else:
            raise ValueError

    @opcode(1)
    def input(self, modes):
        self.set(self.cursor+1, self.input_data.pop(0), modes[0])

    @opcode(1)
    def output(self, modes):
        self.output_data.insert(0, self.get(self.cursor+1, modes[0]))

    @opcode(3)
    def add(self, modes):
        self.set(self.cursor + 3, self.get(self.cursor + 1, modes[0]) + self.get(self.cursor + 2, modes[1]), modes[2])

    @opcode(3)
    def multiply(self, modes):
        self.set(self.cursor + 3, self.get(self.cursor + 1, modes[0]) * self.get(self.cursor + 2, modes[1]), modes[2])


def main():
    with open('input.txt') as f:
        instructions = f.readline()

    comp = IntCodeComputer2(instructions, [1])
    # comp.input_data = [1]
    comp.execute()
    if all([v == 0 for v in comp.output_data[1:]]):
        print('All tests succeeded')
    else:
        raise ValueError
    print(f'Diagnostic code is {comp.output_data[0]}')


if __name__ == '__main__':
    main()