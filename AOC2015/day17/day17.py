import itertools


def get_combos(sizes, target_size):
    iterator = itertools.chain.from_iterable((itertools.combinations(sizes, i) for i in range(1, len(sizes))))
    combos = [tuple(c) for c in iterator if sum(c) == target_size]
    return combos


def main():
    target_size = 150
    with open('input.txt') as f:
        strings = f.readlines()
    sizes = [int(s.strip()) for s in strings]
    combos = get_combos(sizes, target_size)
    print(f'Part 1: Number of combinations is {len(combos)}')

    min_number = min([len(c) for c in combos])
    print(f'Minimum number of containers is {min_number}')
    min_combos = [c for c in combos if len(c) == min_number]
    print(f'Part 2: Number of combinations with {min_number} containers is {len(min_combos)}')


if __name__ == '__main__':
    main()