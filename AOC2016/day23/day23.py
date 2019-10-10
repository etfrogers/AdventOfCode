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
        if value == '91' or value == '85':
            # print(f'Comparator {comparator}, jump size {jump_size}')
            print(f'Copying value {value} to {register}')
            print(self.register_string)
        if self.is_valid_register(register):
            super().copy(value, register)

    def inc(self, register):
        if self.is_valid_register(register):
            super().inc(register)

    def dec(self, register):
        if self.is_valid_register(register):
            super().dec(register)

    def jnz(self, comparator, jump_size):
        if comparator == 91 or comparator == 1:
            print(f'Comparator {comparator}, jump size {jump_size}')
        super().jnz(comparator, jump_size)

    def toggle(self, offset):
        print(f'Offset is {offset}, value: {self.get_value(offset)}')
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


def python_translation(a):
    b = a  # cpy a b
    b -= 1  # dec b
    i = 0
    while True:
        d = a  # cpy a d
        a = 0  # cpy 0 a
        while d != 0:
            c = b  # cpy b c
            while c != 0:
                a += 1  # inc a
                c -= 1  # dec c
                # jnz c -2
            d -= 1  # dec d
            # jnz d -5
        b -= 1  # dec b
        c = b  # cpy b c
        d = c  # cpy c d
        while d != 0:
            d -= 1  # dec d
            c += 1  # inc c
            # jnz d -2
        i += 1  # tgl c
        # cpy -16 c
        # jnz 1 c # offset 2
        if i >= 5:
            c = 1
            break
    c = 85  # cpy 85 c
    while True:
        if i >= 3:
            d = 91  # jnz 91 d # offset 4
        else:
            raise NotImplementedError
        while True:
            a += 1  # inc a
            d += (-1 if i >= 2 else 1)  # inc d # offset 6
            if d == 0:  # jnz d -2
                break
        c += (-1 if i >= 1 else 1)  # inc c # offset 8
        if c == 0:  # jnz c -5
            break
    return a


def main():
    with open('input.txt') as file:
        prog = file.readlines()
    interp = AssemBunnyInterpreter23(prog)
    interp.registers['a'] = 7
    interp.execute(show_status=False)
    print('Part 1: Value of a is ', interp.registers['a'])

    interp2 = AssemBunnyInterpreter23(prog)
    interp2.registers['a'] = 12
    interp2.execute(show_status=True)
    print('Part 2: Value of a is ', interp2.registers['a'])


if __name__ == '__main__':
    main()
