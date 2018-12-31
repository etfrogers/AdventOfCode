import time

from AOC2018.day16 import day16
from AOC2018.day19 import assembly


class JumpDevice(day16.Device):
    def __init__(self, n_registers=6):
        super().__init__(n_registers)
        self.instruction_pointer = 0
        self.opcodes['#ip'] = None
        self.log = []

    def run(self, program, limit=None, registers=None, do_print=False, log_at_line=None):
        self.reset()
        if registers is not None:
            self.registers = registers
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
            if log_at_line and log_at_line == ip:
                self.log.append(self.registers)
            self.registers[self.instruction_pointer] = ip
            self.execute_line(line)
            ip = self.registers[self.instruction_pointer]
            ip += 1
            counter += 1
            if do_print:
                print(f'{line[0]}: {line[1:]} -> {self.registers}')
                # time.sleep(0.3)
        return counter


def main():
    with open('input.txt') as f:
        program = f.read()
    device = JumpDevice()
    device.run(program, do_print=False)
    print('Part 1: ', device.registers)
    print('Part 1 direct: ', assembly.run_direct(part2=False))

    # device.reset()
    # registers = [1] + [0] * 5
    # device.run(program, registers=registers, do_print=True)
    # print('Part 2: ', device.registers)

    print('Part 2: ', assembly.run_direct(part2=True))


if __name__ == '__main__':
    main()

