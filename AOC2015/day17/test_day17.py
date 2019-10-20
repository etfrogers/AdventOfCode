from AOC2015.day17.day17 import get_combos

test_sizes = [20, 15, 10, 5, 5]


def test_1():
    target_size = 25
    combos = get_combos(test_sizes, target_size)
    assert len(combos) == 4
    combos = [tuple(sorted(c)) for c in combos]
    assert (10, 15) in combos
    assert (5, 5, 15) in combos
    assert (5, 20) in combos
    assert combos.count((5, 20)) == 2


def test_2():
    target_size = 25
    combos = get_combos(test_sizes, target_size)
    min_number = min([len(c) for c in combos])
    min_combos = [c for c in combos if len(c) == min_number]
    assert len(min_combos) == 3


def test_part1():
    target_size = 150
    with open('input.txt') as f:
        strings = f.readlines()
    sizes = [int(s.strip()) for s in strings]
    combos = get_combos(sizes, target_size)
    assert len(combos) == 1304


def test_part2():
    target_size = 150
    with open('input.txt') as f:
        strings = f.readlines()
    sizes = [int(s.strip()) for s in strings]
    combos = get_combos(sizes, target_size)

    min_number = min([len(c) for c in combos])
    assert min_number == 4
    min_combos = [c for c in combos if len(c) == min_number]
    assert len(min_combos) == 18

