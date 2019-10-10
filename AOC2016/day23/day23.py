from AOC2016.day12.day12 import AssemBunnyInterpreter


class AssemBunnyInterpreter23(AssemBunnyInterpreter):
    VALID_REGISTERS = {'a', 'b', 'c', 'd'}

    def __init__(self, instruction_list):
        self.instruction_dict = {'cpy': self.copy,
                                 'inc': self.inc,
                                 'dec': self.dec,
                                 'jnz': self.jnz,
                                 'tgl': self.toggle}
        super(AssemBunnyInterpreter, self).__init__(instruction_list)

    def copy(self, value, register):
        if self.is_valid_register(register):
            super().copy(value, register)

    def inc(self, register):
        if self.is_valid_register(register):
            super().inc(register)

    def dec(self, register):
        if self.is_valid_register(register):
            super().dec(register)

    def toggle(self, offset):
        try:
            instruction = self.instructions[self.pointer + self.get_value(offset)]
        except IndexError:
            return
        if len(instruction['args']) == 1:
            if instruction['func'] == self.inc:
                instruction['func'] = self.dec
            else:
                instruction['func'] = self.inc
        elif len(instruction['args']) == 2:
            if instruction['func'] == self.jnz:
                instruction['func'] = self.copy
            else:
                instruction['func'] = self.jnz
        else:
            raise TypeError('Unexpected number of arguments')

    @staticmethod
    def is_valid_register(register):
        return register in AssemBunnyInterpreter23.VALID_REGISTERS


def main():
    with open('input.txt') as file:
        prog = file.readlines()
    interp = AssemBunnyInterpreter23(prog)
    interp.registers['a'] = 7
    interp.execute(show_status=True)
    print('Part 1: Value of a is ', interp.registers['a'])


if __name__ == '__main__':
    main()
