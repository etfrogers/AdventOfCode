from AOC2019.day2.day2 import opcode
from AOC2019.day7.day7 import AsyncIntCodeComputer


class IntCodeInstructions:
    def __init__(self, instructions):
        self.list = instructions
    
    def __getitem__(self, item):
        self.verify_long_enough(item)
        return self.list[item]

    def __setitem__(self, key, value):
        self.verify_long_enough(key)
        self.list[key] = value

    def verify_long_enough(self, length):
        difference = length + 1 - len(self.list)
        if difference > 0:
            self.list += [0] * difference


class RelativeIntCodeComputer(AsyncIntCodeComputer):
    def __init__(self, instructions, input_=None):
        super().__init__(instructions, input_)
        self.opcodes[9] = self.adjust_relative_base
        self.relative_base = 0
        self.instructions = IntCodeInstructions(self.parse_instructions(instructions))
        
    @opcode(1)
    def adjust_relative_base(self, modes):
        self.relative_base += self.get(self.cursor + 1, modes[0])

    def get(self, index, mode):
        if mode == 2:
            return self.instructions[self.relative_base + self.instructions[index]]
        else:
            return super().get(index, mode)

    def set(self, index, value, mode):
        if mode == 2:
            self.instructions[self.relative_base + self.instructions[index]] = value
        else:
            super().set(index, value, mode)


def main():
    with open('input.txt') as f:
        instructions = f.readline()

    comp = RelativeIntCodeComputer(instructions, [1])
    comp.execute()
    assert len(comp.output_data) == 1
    print(f'BOOST keycode: {comp.output_data[0]}')

    comp = RelativeIntCodeComputer(instructions, [2])
    comp.execute()
    assert len(comp.output_data) == 1
    print(f'Coordinates: {comp.output_data[0]}')


if __name__ == '__main__':
    main()
