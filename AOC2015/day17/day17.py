import itertools


def get_combos(sizes, target_size):
    combos = []
    for i in range(1, len(sizes)):
        combos.extend((tuple(c) for c in itertools.combinations(sizes, i) if sum(c) == target_size))
    return combos


def main():
    target_size = 150
    with open('input.txt') as f:
        strings = f.readlines()
    sizes = [int(s.strip()) for s in strings]
    combos = get_combos(sizes, target_size)
    print(f'Part 1: number of combinations is {len(combos)}')



if __name__ == '__main__':
    main()