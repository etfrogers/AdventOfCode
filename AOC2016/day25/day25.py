from AOC2016.day12.day12 import AssemBunnyInterpreter
from AOC2016.day23.day23 import AssemBunnyInterpreter23


class AssemBunnyInterpreter25(AssemBunnyInterpreter23):
    def __init__(self, instruction_list, abort_on_mismatch=True):
        self.instruction_dict = {'cpy': self.copy,
                                 'inc': self.inc,
                                 'dec': self.dec,
                                 'jnz': self.jnz,
                                 'tgl': self.toggle,
                                 'out': self.output_value}
        self.output = []
        self.output_limit = 1000000
        self.abort_on_mismatch = abort_on_mismatch
        super(AssemBunnyInterpreter, self).__init__(instruction_list)

    def output_value(self, value):
        self.output.append(self.get_value(value))
        # print(self.output)
        if ((not (all([v == i % 2 for i, v in enumerate(self.output)])) and self.abort_on_mismatch)
                or len(self.output) > self.output_limit):
            return self.output

    def jnz(self, comparator, jump_size):
        if comparator == '0':
            print(self.register_string)
        super(AssemBunnyInterpreter25, self).jnz(comparator, jump_size)


def main():
    with open('input.txt') as file:
        prog = file.readlines()
    interp = AssemBunnyInterpreter25(prog)
    for a in range(1, 100000):
        print(f'Trying a={a}')
        interp.registers['a'] = a
        interp.execute(show_status=False)
        if len(interp.output) == interp.output_limit:
            print(f'Found a ={a} works for 1,000,000 outputs')
            break
    # print('Part 1: Value of a is ', interp.registers['a'])


def python_translation(a, n_output):
    output = []
    d = a  # cpy a d
    c = 11  # cpy 11 c
    while True:
        b = 231  # cpy 231 b
        while True:
            d += 1  # inc d
            b -= 1  # dec b
            if b == 0:  # jnz b -2
                break
        c -= 1  # dec c
        if c == 0:  # jnz c -5
            break
    while True:
        a = d  # cpy d a
        breakout = False
        while True:
            # jnz 0 0 - NOOP
            b = a  # cpy a b
            a = 0  # cpy 0 a
            while True:
                c = 2  # cpy 2 c
                a += 1  # inc a
                while True:
                    if b == 0:  # jnz b 2
                        breakout = True
                        break  # jnz 1 6
                    b -= 1  # dec b
                    c -= 1  # dec c
                    if c == 0:  # jnz c -4
                        break
                if breakout:
                    break
                # jnz 1 -7
            # if b == 0:?
            b = 2  # cpy 2 b
            while True:
                if c == 0:  # jnz c 2
                    break  # jnz 1 4
                b -= 1  # dec b
                c -= 1  # dec c
                # jnz 1 -4
            # jnz 0 0 - NOOP
            output.append(b)  # out b
            if len(output) >= n_output:
                return output
            if a == 0:  # jnz a -19
                break
        # jnz 1 -21


if __name__ == '__main__':
    main()
