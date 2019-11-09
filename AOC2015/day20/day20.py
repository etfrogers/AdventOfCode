import itertools


def factors(n):
    flatten_iter = itertools.chain.from_iterable
    factors = set(flatten_iter((i, n // i) for i in range(1, int(n ** 0.5) + 1) if n % i == 0))
    return factors


def how_many_presents(n):
    return 10*sum(factors(n))


def min_house(presents, print_=False):
    n = 1
    while (p := how_many_presents(n)) < presents:
        if print_ and n % 1000 == 0:
            print(f'{n}: {p}')
        n += 1
    return n


def main():
    presents = 29000000
    n = min_house(presents)

    print(f'Part 1: Minimum house with {presents} presents is {n}')


if __name__ == '__main__':
    main()
