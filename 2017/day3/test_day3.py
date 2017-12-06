# from nose.tools import *
import day3


def test_manhattan_dist1():
    assert day3.manhattan_dist((0, 0), (0, 0)) == 0


def test_manhattan_dist2():
    assert day3.manhattan_dist((2, 1), (0, 0)) == 3


def test_manhattan_dist3():
    assert day3.manhattan_dist((0, -2), (0, 0)) == 2


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
