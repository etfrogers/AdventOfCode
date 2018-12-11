import day1


def test1():
    input = '+1, -2, +3, +1'
    v = day1.parse_frequency_changes(0, input)
    assert v == 3


def test2():
    input = '+1, +1, +1'
    v = day1.parse_frequency_changes(0, input)
    assert v == 3


def test3():
    input = '+1, +1, -2'
    v = day1.parse_frequency_changes(0, input)
    assert v == 0


def test4():
    input = '-1, -2, -3'
    v = day1.parse_frequency_changes(0, input)
    assert v == -6


def test_part2_1():
    input = '+1, -2, +3, +1'
    v = day1.find_repeated_freq(0, input)
    assert v == 2


def test_part2_2():
    input = '+1, -1'
    v = day1.find_repeated_freq(0, input)
    assert v == 0


def test_part2_3():
    input = '+3, +3, +4, -2, -4'
    v = day1.find_repeated_freq(0, input)
    assert v == 10


def test_part2_4():
    input = '-6, +3, +8, +5, -6'
    v = day1.find_repeated_freq(0, input)
    assert v == 5


def test_part2_5():
    input = '+7, +7, -2, -7, -4'
    v = day1.find_repeated_freq(0, input)
    assert v == 14

