import copy
import math
from collections import defaultdict, deque
from typing import Tuple, Dict, Union

import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    @property
    def tuple(self):
        return tuple(self)

    def __add__(self, other):
        return Point(*[v1 + v2 for v1, v2 in zip(self, other)])

    def __sub__(self, other):
        return Point(*[v1 - v2 for v1, v2 in zip(self, other)])

    def __iadd__(self, other):
        for key in self.__dict__.keys():
            self.__dict__[key] += other.__dict__[key]
        return self

    def __isub__(self, other):
        for key in self.__dict__.keys():
            self.__dict__[key] -= other.__dict__[key]
        return self

    def __eq__(self, other):
        return all([v1 == v2 for v1, v2 in zip(self, other)])

    def __repr__(self):
        return f'<Point(' + ', '.join([str(v) for v in self]) + ')>'

    def norm(self, order=2):
        return sum([abs(v)**order for v in self])

    @staticmethod
    def manhattan_dist(pt1, pt2) -> int:
        return (pt2 - pt1).norm(order=1)

    @staticmethod
    def dist(pt1, pt2) -> int:
        return (pt2 - pt1).norm(order=2)

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
    """You can initialize my value but not change it. Any access to the variable returns a copy"""
    def __init__(self, value):
        self.value = value

    def __get__(self, obj, type=None):
        return copy.copy(self.value)

    def __set__(self, obj, val):
        pass


class DirectionNP(Direction):
    def turn_left(self):
        curr = self
        if curr == DirectionsNP.NORTH:
            new = DirectionsNP.WEST
        elif curr == DirectionsNP.WEST:
            new = DirectionsNP.SOUTH
        elif curr == DirectionsNP.SOUTH:
            new = DirectionsNP.EAST
        elif curr == DirectionsNP.EAST:
            new = DirectionsNP.NORTH
        else:
            raise ValueError
        self.x, self.y = new.x, new.y

    def turn_right(self):
        curr = self
        if curr == DirectionsNP.NORTH:
            new = DirectionsNP.EAST
        elif curr == DirectionsNP.EAST:
            new = DirectionsNP.SOUTH
        elif curr == DirectionsNP.SOUTH:
            new = DirectionsNP.WEST
        elif curr == DirectionsNP.WEST:
            new = DirectionsNP.NORTH
        else:
            raise ValueError
        self.x, self.y = new.x, new.y


class DirectionsNP:
    NORTH = CopyAttribute(DirectionNP(0, -1))
    EAST = CopyAttribute(DirectionNP(1, 0))
    SOUTH = CopyAttribute(DirectionNP(0, 1))
    WEST = CopyAttribute(DirectionNP(-1, 0))


class Directions:
    NORTH = CopyAttribute(Direction(0, 1))
    EAST = CopyAttribute(Direction(1, 0))
    SOUTH = CopyAttribute(Direction(0, -1))
    WEST = CopyAttribute(Direction(-1, 0))

    def __iter__(self):
        for direction in [self.NORTH, self.SOUTH, self.EAST, self.WEST]:
            yield direction



def coord_map_to_array(map_: Dict[Tuple[int, int], int], override_size:int = None, dtype=int):
    if override_size:
        corner = math.floor(override_size / 2)
        bottom_left = Point(-corner, -corner)
        top_right = Point(corner, corner)
    else:
        xs, ys = zip(*map_.keys())
        bottom_left = Point(min(xs), min(ys))
        top_right = Point(max(xs), max(ys))

    def _to_np_coords(pt: Union[Point, Tuple[int, int]]):
        try:
            out = pt - bottom_left
        except TypeError:
            out = Point(*pt) - bottom_left
        return tuple(reversed(out.tuple))

    size = _to_np_coords(top_right + Point(1, 1))
    array = np.zeros(size, dtype=dtype)
    for key, value in map_.items():
        array[_to_np_coords(key)] = value
    return array


def array_to_string(array: np.ndarray, map_: dict = None, flip=True) -> str:
    if map_:
        str_array = np.full_like(array, '', dtype=str)
        for key, value in map_.items():
            str_array[array == key] = value
    else:
        str_array = array
    if flip:
        str_array = np.flipud(str_array)
    lines = [''.join([str(v) for v in line]) for line in str_array]
    return '\n'.join(lines)


def string_to_array(string: str, map_: dict = None, flip=True, dtype=int) -> np.ndarray:
    list_ = [list(line) for line in string.split('\n')]
    str_array = np.array(list_, dtype=str)
    if map_:
        output = np.zeros_like(str_array, dtype=dtype)
        for key, value in map_.items():
            output[str_array == key] = value
    else:
        output = str_array
    if flip:
        output = np.flipud(output)
    return output


class FIFOQueue:
    def __init__(self, initial_data=None):
        if initial_data is None:
            initial_data = []
        self._data = deque(initial_data)

    def push(self, value):
        self._data.append(value)

    def pop(self):
        return self._data.popleft()

    def __iter__(self):
        return self._data.__iter__()

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]
