import day6


def test_balance_blocks1():
    count, _ = day6.balance_blocks([0, 2, 7, 0])
    assert count == 5


def test_part1():
    input = [4, 1, 15, 12, 0, 9, 9, 5, 5, 8, 7, 3, 14, 5, 12, 3]
    count, _ = day6.balance_blocks(input)
    assert count == 6681
