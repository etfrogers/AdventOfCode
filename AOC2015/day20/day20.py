import itertools
from collections import defaultdict


def factors(n):
    flatten_iter = itertools.chain.from_iterable
    return set(flatten_iter((i, n // i) for i in range(1, int(n ** 0.5) + 1) if n % i == 0))


def how_many_presents(n, part2=False):
    if part2:
        raise NotImplementedError
    return 10*sum(factors(n))


def how_many_presents_iter(limit=1000, part2=False):
    working_elves = defaultdict(int)
    if part2:
        presents_per_elf = 11
    else:
        presents_per_elf = 10
    for n in range(limit):
        factors_ = factors(n)
        if part2:
            for f in factors_:
                working_elves[f] += 1
            for elf in list(working_elves.keys()):
                if working_elves[elf] >= 51:
                    del working_elves[elf]
            factors_ = [f for f in factors_ if f in working_elves]
        yield presents_per_elf * sum(factors_)


def min_house(presents, print_=False, part2=False):
    if part2:
        n = 1
        for n, p in enumerate(how_many_presents_iter(limit=1000000, part2=part2)):
            if print_ and n % 1000 == 0:
                print(f'{n}: {p}')
            if p > presents:
                break
    else:
        n = 1
        while (p := how_many_presents(n)) < presents:
            if print_ and n % 1000 == 0:
                print(f'{n}: {p}')
            n += 1
    return n


def main():
    presents = 29000000

    # n = min_house(presents, print_=True)
    # print(f'Part 1: Minimum house with {presents} presents is {n}')

    n = min_house(presents, print_=True, part2=True)
    print(f'Part 2: Minimum house with {presents} presents is {n}')


if __name__ == '__main__':
    main()
