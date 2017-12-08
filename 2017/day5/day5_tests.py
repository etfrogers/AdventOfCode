import day5


def test_count_jumps1():
    assert day5.count_jumps([0, 3, 0, 1, -3]) == 5


def test_count_jump_part1():
    with open('input.txt', 'r') as file:
        inst = file.readlines()
    inst = [line.strip() for line in inst]
    inst = [int(l) for l in inst]
    assert day5.count_jumps(inst) == 336905


def test_count_jumps2():
    assert day5.count_jumps([0, 3, 0, 1, -3], True) == 10


def test_count_jump_part2():
    with open('input.txt', 'r') as file:
        inst = file.readlines()
    inst = [line.strip() for line in inst]
    inst = [int(l) for l in inst]
    assert day5.count_jumps(inst, True) == 21985262
