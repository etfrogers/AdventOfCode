import numpy as np

from AOC2017.day2.day2 import checksum


def test1():
    data = [[5, 1, 9, 5],
            [7, 5, 3],
            [2, 4, 6, 8]]
    
    assert checksum(data) == 18


def test_part1():
    data = np.loadtxt('input.txt')
    assert checksum(data) == 43074


def test2():
    data = [[5, 9, 2, 8],
            [9, 4, 7, 3],
            [3, 8, 6, 5]]
    assert checksum(data, True) == 9



