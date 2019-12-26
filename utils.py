import copy
from collections import defaultdict


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def tuple(self):
        return self.x, self.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def manhattan_dist(pt1, pt2) -> int:
        diff = [pt1.x - pt2.x, pt1.y - pt2.y]
        abs_diff = [abs(n) for n in diff]
        return sum(abs_diff)

    def move(self, pos):
        self += pos

    def get_pos_after_move(self, pos):
        new = copy.copy(self)
        new.move(pos)
        return new


class KeyDefaultDict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


class Direction(Point):

    def __init__(self, x, y):
        assert abs(x) + abs(y) == 1
        assert x == 0 or y == 0
        super().__init__(x, y)

    def get_hv(self):
        if self.x == 0:
            return 'v'
        elif self.y == 0:
            return 'h'

    def turn_left(self):
        curr = self
        if curr == Directions.NORTH:
            new = Directions.WEST
        elif curr == Directions.WEST:
            new = Directions.SOUTH
        elif curr == Directions.SOUTH:
            new = Directions.EAST
        elif curr == Directions.EAST:
            new = Directions.NORTH
        else:
            raise ValueError
        self.x, self.y = new.x, new.y

    def turn_right(self):
        curr = self
        if curr == Directions.NORTH:
            new = Directions.EAST
        elif curr == Directions.EAST:
            new = Directions.SOUTH
        elif curr == Directions.SOUTH:
            new = Directions.WEST
        elif curr == Directions.WEST:
            new = Directions.NORTH
        else:
            raise ValueError
        self.x, self.y = new.x, new.y

    def get_dir_after_left_turn(self):
        new = copy.copy(self)
        new.turn_left()
        return new

    def get_dir_after_right_turn(self):
        new = copy.copy(self)
        new.turn_right()
        return new

    def reverse(self):
        self.x = -self.x
        self.y = -self.y


class CopyAttribute(object):
    """You can initialize my value but not change it."""
    def __init__(self, value):
        self.value = value

    def __get__(self, obj, type=None):
        return copy.copy(self.value)

    def __set__(self, obj, val):
        pass


class DirectionsNP:
    NORTH = CopyAttribute(Direction(0, -1))
    EAST = CopyAttribute(Direction(1, 0))
    SOUTH = CopyAttribute(Direction(0, 1))
    WEST = CopyAttribute(Direction(-1, 0))


class Directions:
    NORTH = CopyAttribute(Direction(0, 1))
    EAST = CopyAttribute(Direction(1, 0))
    SOUTH = CopyAttribute(Direction(0, -1))
    WEST = CopyAttribute(Direction(-1, 0))

