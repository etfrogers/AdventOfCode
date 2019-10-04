from assembly_interpreter import AssemblyInterpreter


class AssemBunnyInterpreter(AssemblyInterpreter):
    def __init__(self, instruction_list):
        self.instruction_dict = {'cpy': self.copy,
                                 'inc': self.inc,
                                 'dec': self.dec,
                                 'jnz': self.jnz}
        super().__init__(instruction_list)

    def copy(self, value, register):
        self.registers[register] = self.get_value(value)

    def inc(self, register):
        self.registers[register] += 1

    def dec(self, register):
        self.registers[register] -= 1

    def jnz(self, comparator, jump_size):
        if self.get_value(comparator) != 0:
            self.pointer += self.get_value(jump_size) - 1


def main():
    with open('input.txt') as file:
        prog = file.readlines()
    interp = AssemBunnyInterpreter(prog)
    interp.execute()
    print('Part 1: Value of a is ', interp.registers['a'])

    interp2 = AssemBunnyInterpreter(prog)
    interp2.registers['c'] = 1
    interp2.execute()
    print('Part 2: Value of a is ', interp2.registers['a'])


if __name__ == '__main__':
    main()
