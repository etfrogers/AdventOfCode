from collections import deque

from AOC2019.day2.day2 import IntCodeComputer, opcode


class FIFOQueue:
    def __init__(self, initial_data=None):
        if initial_data is None:
            initial_data = []
        self._data = deque(initial_data)

    def push(self, value):
        self._data.append(value)

    def pop(self):
        return self._data.popleft()

    def __iter__(self):
        return self._data.__iter__()

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]

class IntCodeComputer2(IntCodeComputer):
    def __init__(self, instructions, input_=None):
        super().__init__(instructions)
        self.opcodes = {1: self.add,
                        2: self.multiply,
                        99: self.halt,
                        3: self.input,
                        4: self.output,
                        5: self.jump_if_true,
                        6: self.jump_if_false,
                        7: self.less_than,
                        8: self.equals,
                        }
        self.input_data = FIFOQueue(input_)
        self.output_data = FIFOQueue()

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
        self.set(self.cursor+1, self.input_data.pop(), modes[0])

    @opcode(1)
    def output(self, modes):
        self.output_data.push(self.get(self.cursor+1, modes[0]))

    @opcode(3)
    def add(self, modes):
        self.set(self.cursor + 3, self.get(self.cursor + 1, modes[0]) + self.get(self.cursor + 2, modes[1]), modes[2])

    @opcode(3)
    def multiply(self, modes):
        self.set(self.cursor + 3, self.get(self.cursor + 1, modes[0]) * self.get(self.cursor + 2, modes[1]), modes[2])

    @opcode(2)
    def jump_if_true(self, modes):
        if self.get(self.cursor + 1, modes[0]) != 0:
            self.cursor = self.get(self.cursor + 2, modes[1])
            self.cursor -= 3  # to undo the increment that happens automatically due to the opcode decorator

    @opcode(2)
    def jump_if_false(self, modes):
        if self.get(self.cursor + 1, modes[0]) == 0:
            self.cursor = self.get(self.cursor + 2, modes[1])
            self.cursor -= 3  # to undo the increment that happens automatically due to the opcode decorator

    @opcode(3)
    def less_than(self, modes):
        self.set(self.cursor + 3,
                 int(self.get(self.cursor + 1, modes[0]) < self.get(self.cursor + 2, modes[1])),
                 modes[2])

    @opcode(3)
    def equals(self, modes):
        self.set(self.cursor + 3,
                 int(self.get(self.cursor + 1, modes[0]) == self.get(self.cursor + 2, modes[1])),
                 modes[2])


def main():
    with open('input.txt') as f:
        instructions = f.readline()

    comp = IntCodeComputer2(instructions, [1])
    comp.execute()
    if all([v == 0 for v in comp.output_data[1:]]):
        print('All tests succeeded')
    else:
        raise ValueError
    print(f'Diagnostic code for system 1 is {comp.output_data[0]}')

    comp = IntCodeComputer2(instructions, [5])
    comp.execute()
    print(f'Diagnostic code for system 5 is {comp.output_data[0]}')


if __name__ == '__main__':
    main()
