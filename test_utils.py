from utils import Point, Directions


def test_manhattan_dist1():
    assert Point.manhattan_dist(Point(0, 0), Point(0, 0)) == 0


def test_manhattan_dist2():
    assert Point.manhattan_dist(Point(2, 1), Point(0, 0)) == 3


def test_manhattan_dist3():
    assert Point.manhattan_dist(Point(0, -2), Point(0, 0)) == 2


def test_immutability():
    d1 = Directions.NORTH
    d2 = Directions.NORTH
    assert d1 is not d2
    assert d1 == d2
    d1.turn_left()
    assert not d1 == d2
    d2.turn_left()
    assert d1 == d2
