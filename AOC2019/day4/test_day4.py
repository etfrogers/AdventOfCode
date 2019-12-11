import pytest

from AOC2019.day4.day4 import is_valid

cases = [('111111', True),
         ('223450', False),
         ('123789', False)
         ]

cases2 = [('112233', True),
          ('123444', False),
          ('111122', True),
          ('111111', False),
          ('123789', False),
          ('112354', False),
          ('112345', True),
          ('113222', False),
          ('112333', True),
          ]

input_ = (236491, 713787)


@pytest.mark.parametrize('pw, valid', cases)
def test_1(pw, valid):
    assert is_valid(pw) == valid


def test_part1():
    counter = 0
    for i in range(input_[0], input_[1] + 1):
        password = str(i)
        if is_valid(password):
            counter += 1
    assert counter == 1169


@pytest.mark.parametrize('pw, valid', cases2)
def test_2(pw, valid):
    assert is_valid(pw, part2=True) == valid


def test_part2():
    counter = 0
    for i in range(input_[0], input_[1] + 1):
        password = str(i)
        if is_valid(password, part2=True):
            counter += 1
    assert counter == 757
