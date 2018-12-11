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
