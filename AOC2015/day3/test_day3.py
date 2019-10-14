from AOC2015.day3.day3 import get_number_of_unique_houses, get_visits


def test_1():
    instructions = '>'
    houses = get_visits(instructions)
    n_houses = get_number_of_unique_houses(houses)
    assert n_houses == 2


def test_2():
    instructions = '^>v<'
    houses = get_visits(instructions)
    n_houses = get_number_of_unique_houses(houses)
    assert n_houses == 4


def test_3():
    instructions = '^v^v^v^v^v'
    houses = get_visits(instructions)
    n_houses = get_number_of_unique_houses(houses)
    assert n_houses == 2


def test_part2_1():
    instructions = '^v'
    houses = get_visits(instructions, part2=True)
    n_houses = get_number_of_unique_houses(houses)
    assert n_houses == 3


def test_part2_2():
    instructions = '^>v<'
    houses = get_visits(instructions, part2=True)
    n_houses = get_number_of_unique_houses(houses)
    assert n_houses == 3


def test_part2_3():
    instructions = '^v^v^v^v^v'
    houses = get_visits(instructions, part2=True)
    n_houses = get_number_of_unique_houses(houses)
    assert n_houses == 11
