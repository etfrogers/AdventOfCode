from assembly_interpreter import AssemblyInterpreter


class Interpreter2015(AssemblyInterpreter):
    def __init__(self, instruction_list):
        self.instruction_dict = {'hlf': self.half,
                                 'tpl': self.triple,
                                 'inc': self.inc,
                                 'jmp': self.jump,
                                 'jie': self.jump_if_even,
                                 'jio': self.jump_if_one,
                                 }
        super().__init__(instruction_list)

    def half(self, register):
        self.registers[register] /= 2

    def triple(self, register):
        self.registers[register] *= 3

    def inc(self, register):
        self.registers[register] += 1

    def jump(self, offset):
        self.pointer += self.get_value(offset) - 1

    def jump_if_even(self, value, offset):
        if self.get_value(value) % 2 == 0:
            self.jump(offset)

    def jump_if_one(self, value, offset):
        if self.get_value(value) == 1:
            self.jump(offset)

    def get_value(self, value):
        return super().get_value(value.rstrip(','))


def main():
    with open('input.txt') as f:
        instructions = f.readlines()
    interp = Interpreter2015(instructions)
    interp.execute()
    print(f'Part 1: Value in register b is {interp.registers["b"]}')

    interp2 = Interpreter2015(instructions)
    interp2.registers['a'] = 1
    interp2.execute()
    print(f'Part 2: Value in register b is {interp2.registers["b"]}')


if __name__ == '__main__':
    main()
