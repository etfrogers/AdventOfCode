import day6

# noinspection PyShadowingBuiltins
input = [4, 1, 15, 12, 0, 9, 9, 5, 5, 8, 7, 3, 14, 5, 12, 3]


def test_balance_blocks1():
    count, _, _ = day6.balance_blocks([0, 2, 7, 0])
    assert count == 5


def test_part1():
    count, _, _ = day6.balance_blocks(input)
    assert count == 6681


def test_balance_blocks2():
    _, loop_length, _ = day6.balance_blocks([0, 2, 7, 0])
    assert loop_length == 4


def test_part2():
    _, loop_length, _ = day6.balance_blocks(input)
    assert loop_length == 2392
