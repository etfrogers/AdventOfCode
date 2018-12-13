import day5


def test1():
    input = 'aA'
    remainder = day5.reduce(input)
    assert len(remainder) == 0


def test2():
    input = 'abBA'
    remainder = day5.reduce(input)
    assert len(remainder) == 0


def test3():
    input = 'abAB'
    remainder = day5.reduce(input)
    assert len(remainder) == 4


def test4():
    input = 'aabAAb'
    remainder = day5.reduce(input)
    assert len(remainder) == 6


def test5():
    input = 'dabAcCaCBAcCcaDA'
    remainder = day5.reduce(input)
    assert len(remainder) == 10


def test_part2():
    input = 'dabAcCaCBAcCcaDA'
    min_length = day5.check_problems(input)
    assert min_length == 4
