import math
from typing import Tuple, List

import numpy as np

# class Direction(Enum):
#     NORTH = (0, 1)
#     SOUTH = (0, -1)
#     EAST = (1, 0)
#     WEST = (-1, 0)
#
#     def turn_left(self):
#         if self == Direction.NORTH:
#             out = Direction.WEST
#         elif self == Direction.WEST:
#             out = Direction.SOUTH
#         elif self == Direction.SOUTH:
#             out = Direction.EAST
#         elif self == Direction.EAST:
#             out = Direction.NORTH
#         else:
#             raise ValueError
#         return out
from utils import Point, Directions


class SpiralMemory:
    def __init__(self, size: int):
        self._size = size
        self._data = np.zeros((size, size), dtype=np.int)

    def fill_to_value(self, n: int) -> Tuple[int, int]:
        pos = Point(0, 0)
        direct = Directions.EAST
        val = 1
        old_pos = pos
        while val <= n:
            self.set_val(pos, val)
            val += 1
            old_pos = pos
            pos = direct.get_pos_after_move(pos)
            pos_to_left = direct.get_dir_after_left_turn().get_pos_after_move(pos)
            if self.get_val(pos_to_left) is None or self.get_val(pos_to_left) == 0:
                direct.turn_left()
            # print(mem)
        return old_pos

    def stress_test_to_val(self, n: int) -> int:
        pos = Point(0, 0)
        direct = Directions.EAST
        val = 1
        while val <= n:
            self.set_val(pos, val)
            pos = direct.get_pos_after_move(pos)
            val = self.sum_of_neighbours(pos)
            pos_to_left = direct.get_dir_after_left_turn().get_pos_after_move(pos)
            if self.get_val(pos_to_left) is None or self.get_val(pos_to_left) == 0:
                direct.turn_left()
            # print(self)
        return val

    def sum_of_neighbours(self, pos: Point) -> int:
        nbours = self.get_neighbours(pos)
        nbour_values = [self.get_val(n) for n in nbours]
        return sum(nbour_values)

    def get_neighbours(self, pos: Point) -> List[Point]:
        all_neighbours = [pos + Point(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]]
        neighbours_local = [self._to_local_units(p) for p in all_neighbours]
        neighbours = [n for (n, c) in zip(all_neighbours, neighbours_local) if self.in_bounds(c)]
        return neighbours

    def in_bounds(self, pos: Point):
        return (pos.x > 0 and pos.y > 0) and (pos.x < self._size and pos.y < self._size)

    # get_val and set_val take pos in units such that (0, 0) is the centre
    def set_val(self, pos: Point, val: int):
        local_pos = self._to_local_units(pos)
        self._data[local_pos.tuple] = val

    def get_val(self, pos: Point) -> int:
        local_pos = self._to_local_units(pos)
        if self.in_bounds(local_pos):
            value = self._data[local_pos.tuple]
        else:
            value = None
        return value

    @property
    def data(self):
        return self._data

    @property
    def _offset(self) -> Point:
        ov = int(math.floor(self._size/2))
        return Point(ov, ov)

    def _to_local_units(self, pos: Point) -> Point:
        new_pos = pos + self._offset
        return new_pos

    def __str__(self):
        return str(self._data)


def get_turn(n: int) -> int:
    turn = int(math.ceil(math.sqrt(n)))
    if turn % 2 == 0:  # force turn to be an odd number
        turn += 1
    return turn


# def add_pos(pt1: Tuple[int, int], pt2: Tuple[int, int]) -> Tuple[int, int]:
#     return pt1[0]+pt2[0], pt1[1]+pt2[1]


def spiral_distance_quick(n: int) -> int:
    if n == 1:
        return 0
    turn = get_turn(n)
    pts_in_prev_spirals = (turn-2)**2  # -2 because spirals are all odd numbers
    pts_along_spiral = n - pts_in_prev_spirals
    pts_left = pts_along_spiral-1
    start_coord = int((turn-1)/2)
    pos = Point(start_coord, -(start_coord-1))

    direct = Directions.NORTH
    pts_moved = 0
    while pts_left > 0:
        pts_left -= 1
        pts_moved += 1
        pos = direct.get_pos_after_move(pos)
        if (direct == Directions.NORTH and pts_moved >= turn-2) or pts_moved >= turn-1:
            pts_moved = 0
            direct.turn_left()

    dist = Point.manhattan_dist(pos, Point(0, 0))
    return dist


def spiral_distance_full(n: int) -> int:
    outer_turn = get_turn(n)
    mem = SpiralMemory(outer_turn)
    pos = mem.fill_to_value(n)

    dist = Point.manhattan_dist(pos, Point(0, 0))
    return dist


def stress_test(n: int) -> int:
    outer_turn = get_turn(n)
    mem = SpiralMemory(outer_turn)
    output = mem.stress_test_to_val(n)
    return output


def spiral_distance(n: int, full_spiral: bool = False) -> int:
    if full_spiral:
        dist = spiral_distance_full(n)
    else:
        dist = spiral_distance_quick(n)
    return dist


def main() -> int:
    input_n = 368078
    dist = stress_test(input_n)
    # dist = spiral_distance(input_n, True)
    print(dist)
    return 0


if __name__ == '__main__':
    main()
