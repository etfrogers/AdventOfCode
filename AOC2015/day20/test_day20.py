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


@pytest.mark.parametrize('h, p', tests)
def test_n_presents_numpy(h, p):
    max_presents = max([p for h, p in tests])
    n, houses = min_house(max_presents)
    assert houses[h] == p


@pytest.mark.parametrize('h, p', tests)
def test_n_presents_numpy_part2(h, p):
    max_presents = max([p for h, p in tests])
    n, houses = min_house(max_presents, part2=True)
    assert houses[h] == 11 * p / 10


@pytest.mark.parametrize('i', range(100))
def test_n_presents_numpy_part1_vs_part2(i):
    max_presents = 1000
    n1, houses1 = min_house(max_presents, part2=False)
    n2, houses2 = min_house(max_presents, part2=True)
    adjustment = 0 if i <= 50 else 11
    assert houses2[i] == (11 * houses1[i] / 10) - adjustment


def test_small_presents():
    presents = 150
    n, _ = min_house(presents)
    assert n == 8


def test_part1():
    presents = 29000000
    n, _ = min_house(presents)
    assert n == 665280


def test_part2():
    presents = 29000000
    n, _ = min_house(presents, part2=True)
    assert n == 705600
