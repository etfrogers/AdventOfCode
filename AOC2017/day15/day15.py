
DIVISOR = 2147483647
LOWEST_16_BITS = (2**16) - 1 
FACTOR_A = 16807
FACTOR_B = 48271
PART_1_ITERATIONS = 40000000
PART_2_ITERATIONS = 5000000
PICKY_VAL_A = 4
PICKY_VAL_B = 8


class Generator:
    def __init__(self, factor, start_val, picky_val=None):
        self.factor = factor
        self.last_val = start_val
        self.is_picky = picky_val is not None
        self.picky_val = picky_val

    def __iter__(self):
        return self

    def gen_val(self):
        val = (self.last_val * self.factor) % DIVISOR
        self.last_val = val
        return val

    def __next__(self):
        val = self.gen_val()
        while self.is_picky and val % self.picky_val != 0:
            val = self.gen_val()
        return val


def compare(int1, int2):
    return (int1 & LOWEST_16_BITS) == (int2 & LOWEST_16_BITS)


def count_matches(gen_a, gen_b, n_iterations):
    matches = 0
    for i, valA, valB in zip(range(0, n_iterations), gen_a, gen_b):
        if (i % 100000) == 0:
            print(i)
        # print((valA, valB))
        if compare(valA, valB):
            matches += 1
    return matches


def main():
    # start_a = 65    # test
    # start_b = 8921  # test
    start_a = 679   # real
    start_b = 771   # real

    gen_a = Generator(FACTOR_A, start_a, PICKY_VAL_A)
    gen_b = Generator(FACTOR_B, start_b, PICKY_VAL_B)
    matches = count_matches(gen_a, gen_b, PART_2_ITERATIONS)
    print(matches)


if __name__ == '__main__':
    main()
