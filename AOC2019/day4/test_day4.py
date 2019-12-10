import pytest

from AOC2019.day4.day4 import is_valid

cases = [('111111', True),
         ('223450', False),
         ('123789', False)
         ]


@pytest.mark.parametrize('pw, valid', cases)
def test_1(pw, valid):
    assert is_valid(pw) == valid
