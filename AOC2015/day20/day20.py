import itertools
import numpy as np


def factors(n):
    flatten_iter = itertools.chain.from_iterable
    return set(flatten_iter((i, n // i) for i in range(1, int(n ** 0.5) + 1) if n % i == 0))


def how_many_presents(n, part2=False):
    if part2:
        raise NotImplementedError
    return 10*sum(factors(n))


def min_house(presents, print_=False, part2=False):
    n = presents // 10
    houses = np.zeros((n, ))
    for i in range(1, n):
        if print_ and i % 1000 == 0:
            print(i)
        if part2:
            houses[i:50*i+1:i] += 11 * i
        else:
            houses[i::i] += 10 * i
    lowest_house = np.min(np.where(houses >= presents))
    return lowest_house, houses


def main():
    presents = 29000000

    n, _ = min_house(presents, print_=False)
    print(f'Part 1: Minimum house with {presents} presents is {n}')

    n, _ = min_house(presents, print_=False, part2=True)
    print(f'Part 2: Minimum house with {presents} presents is {n}')


if __name__ == '__main__':
    main()
