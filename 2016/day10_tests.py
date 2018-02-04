import day10


def test_1():
    with open('day10_test_input.txt') as file:
        instructions = file.readlines()
    instructions = [i.strip() for i in instructions]
    factory = day10.Factory(instructions)
    id, _ = factory.get_comparator((2, 5))
    assert id == 2


def test_part1():
    with open('day10_input.txt') as file:
        instructions = file.readlines()
    instructions = [i.strip() for i in instructions]
    factory = day10.Factory(instructions)
    id, _ = factory.get_comparator((17, 61))
    assert id == 93
