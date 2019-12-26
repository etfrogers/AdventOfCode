# from nose.tools import *
import day3

from AOC2017.day3.day3 import stress_test


def test_spiral_distance1():
    assert day3.spiral_distance(1) == 0


def test_spiral_distance2():
    assert day3.spiral_distance(12) == 3


def test_spiral_distance3():
    assert day3.spiral_distance(23) == 2


def test_spiral_distance4():
    assert day3.spiral_distance(1024) == 31


def test_spiral_distance5():
    assert day3.spiral_distance(1, True) == 0


def test_spiral_distance6():
    assert day3.spiral_distance(12, True) == 3


def test_spiral_distance7():
    assert day3.spiral_distance(23, True) == 2


def test_spiral_distance8():
    assert day3.spiral_distance(1024, True) == 31


def test_part1():
    assert day3.spiral_distance(368078, False) == 371


def test_part2():
    input_n = 368078
    dist = stress_test(input_n)
    assert dist == 369601


