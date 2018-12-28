from AOC2018.day16 import day16


class JumpDevice(day16.Device):
    def __init__(self, n_registers=6):
        super().__init__(n_registers)
        self.instruction_pointer = 0
        self.opcodes['#ip'] = None

    def run(self, program, limit=None):
        self.reset()
        program = self.parse_program(program)

        ip_line = program.pop(0)
        assert ip_line[0] is None
        self.instruction_pointer = ip_line[1][0]
        ip = self.registers[self.instruction_pointer]

        counter = 0
        while True:
            if limit is not None and counter >= limit:
                break
            try:
                line = program[ip]
            except IndexError:
                break
            self.registers[self.instruction_pointer] = ip
            self.execute_line(line)
            ip = self.registers[self.instruction_pointer]
            ip += 1
            counter += 1


def main():
    with open('input.txt') as f:
        program = f.read()
    device = JumpDevice()
    device.run(program)
    print('Part 1: ', device.registers)


if __name__ == '__main__':
    main()

