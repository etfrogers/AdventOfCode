from assembly_interpreter import AssemblyInterpreter


class CoProc(AssemblyInterpreter):
    def __init__(self, instruction_list):
        self.mul_count = 0
        self.instruction_dict = {'set': self.set,
                                 'sub': self.subtract,
                                 'mul': self.multiply,
                                 'jnz': self.jump_nz,
                                 }
        super().__init__(instruction_list)

    def set(self, register, value):
        self.registers[register] = self.get_value(value)

    def subtract(self, register, value):
        self.registers[register] -= self.get_value(value)

    def multiply(self, register, value):
        self.mul_count += 1
        self.registers[register] *= self.get_value(value)

    def jump_nz(self, register, value):
        if self.get_value(register) != 0:
            self.pointer += self.get_value(value) - 1


def rawcode():
    mul_counter = 0
    a = b = c = d = e = f = g = h = 0
    b = 84
    c = b
    # a = 1 for part 2
    if a != 0:
        b *= 100; mul_counter += 1
        b -= -100000
        c = b
        c -= -17000
    while True:
        f = 1
        d = 2
        e = 2
        done1 = False
        done2 = False
        while not done2:
            while not done1:
                g = d
                g *= e; mul_counter += 1
                g -= b
                if g == 0:
                    f = 0
                e -= -1
                g = e
                g -= b
                done1 = g == 0
            d -= -1
            g = d
            g -= b
            done2 = g == 0

        if f == 0:
            h -= -1
        g = b
        g -= c

        if g == 0:
            break
        b -= -17
    print(a, b, c, d, e, f, g, h)
    return mul_counter, ()


def rawcode2(b_in=None, end_in=None):

    # noinspection PyUnusedLocal
    a = b = end_search = d = e = found_multiple = g = counter = 0
    a = 1  # for part 2
    # above is Ed's code
    b = 84 if b_in is None else b_in
    end_search = b if end_in is None else end_in
    if not a == 0:  # jnz a 2, jnz 1 5
        b = (b * 100) + 100000
        end_search = b + 17000 if end_in is None else end_in
    while True:
        found_multiple = is_prime(b)
        if found_multiple == 0:
            counter += 1
        if b >= end_search:
            break
        b += 17

    registers = (a, b, end_search, b, b, found_multiple, g, counter)
    return None, registers


primes = set()
with open('primes_to_1million.txt', 'r') as file:
    prime_lines = file.readlines()
for line in prime_lines:
    for p in line.split():
        primes.add(int(p))


def is_prime(b):
    assert b < max(primes)
    return b in primes


def main():
    with open('input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    print(instructions)
    coproc = CoProc(instructions)
    coproc.registers['a'] = 0
    coproc.execute(show_status=False)
    print(coproc.register_string)
    print(coproc.mul_count)
    mul = rawcode2()
    print(mul)


if __name__ == '__main__':
    main()
