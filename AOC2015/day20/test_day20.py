import pytest

from AOC2015.day20.day20 import how_many_presents, min_house

tests = [(1, 10),
         (2, 30),
         (3, 40),
         (4, 70),
         (5, 60),
         (6, 120),
         (7, 80),
         (8, 150),
         (9, 130),
         ]


@pytest.mark.parametrize("n, presents", tests)
def test_1(n, presents):
    assert presents == how_many_presents(n)


def test_part1():
    presents = 29000000
    n = min_house(presents)
    assert n == 665280
