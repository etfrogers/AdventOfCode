import math
from typing import Tuple, List
from enum import Enum
import numpy as np


class Direction(Enum):
    NORTH = (0, 1)
    SOUTH = (0, -1)
    EAST = (1, 0)
    WEST = (-1, 0)

    def turn_left(self):
        if self == Direction.NORTH:
            out = Direction.WEST
        elif self == Direction.WEST:
            out = Direction.SOUTH
        elif self == Direction.SOUTH:
            out = Direction.EAST
        elif self == Direction.EAST:
            out = Direction.NORTH
        else:
            raise ValueError
        return out

    def move(self, pos: Tuple[int, int]):
        return add_pos(pos, self.value)


class SpiralMemory:
    def __init__(self, size):
        self._size = size
        self._data = np.zeros((size, size), dtype=np.int)

    def fill_to_value(self, n: int) -> Tuple[int, int]:
        pos = (0, 0)
        direct = Direction.EAST
        val = 1
        old_pos = pos
        while val <= n:
            self.set_val(pos, val)
            val += 1
            old_pos = pos
            pos = direct.move(pos)
            pos_to_left = direct.turn_left().move(pos)
            if self.get_val(pos_to_left) is None or self.get_val(pos_to_left) == 0:
                direct = direct.turn_left()
            # print(mem)
        return old_pos

    def stress_test_to_val(self, n: int) -> int:
        pos = (0, 0)
        direct = Direction.EAST
        val = 1
        while val <= n:
            self.set_val(pos, val)
            pos = direct.move(pos)
            val = self.sum_of_neighbours(pos)
            pos_to_left = direct.turn_left().move(pos)
            if self.get_val(pos_to_left) is None or self.get_val(pos_to_left) == 0:
                direct = direct.turn_left()
            print(self)
        return val

    def sum_of_neighbours(self, pos: Tuple[int, int]) -> int:
        nbours = self.get_neighbours(pos)
        nbour_values = [self.get_val(n) for n in nbours]
        return sum(nbour_values)

    def get_neighbours(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        all_neighbours = [add_pos(pos, (i, j)) for i in [-1, 0, 1] for j in [-1, 0, 1]]
        neighbours_local = [self._to_local_units(p) for p in all_neighbours]
        neighbours = [n for (n, c) in zip(all_neighbours, neighbours_local) if self.in_bounds(c)]
        return neighbours

    def in_bounds(self, pos):
        return all([c > 0 for c in pos]) and all([c < self._size for c in pos])

    # get_val and set_val take pos in units such that (0, 0) is the centre
    def set_val(self, pos: Tuple[int, int], val: int):
        local_pos = self._to_local_units(pos)
        self._data[local_pos] = val

    def get_val(self, pos: Tuple[int, int]) -> int:
        local_pos = self._to_local_units(pos)
        if self.in_bounds(local_pos):
            value = self._data[local_pos]
        else:
            value = None
        return value


    @property
    def data(self):
        return self._data

    @property
    def _offset(self) -> Tuple[int, int]:
        ov = int(math.floor(self._size/2))
        return ov, ov

    def _to_local_units(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        new_pos = add_pos(pos, self._offset)
        return new_pos[1], new_pos[0]

    def __str__(self):
        return str(self._data)


def manhattan_dist(pt1: Tuple[int, int], pt2: Tuple[int, int]) -> int:
    diff = [c1 - c2 for (c1, c2) in zip(pt1, pt2)]
    abs_diff = [abs(n) for n in diff]
    return sum(abs_diff)


def get_turn(n: int) -> int:
    turn = int(math.ceil(math.sqrt(n)))
    if turn % 2 == 0:  # force turn to be an odd number
        turn += 1
    return turn


def add_pos(pt1: Tuple[int, int], pt2: Tuple[int, int]) -> Tuple[int, int]:
    return pt1[0]+pt2[0], pt1[1]+pt2[1]


def spiral_distance_quick(n: int) -> int:
    if n == 1:
        return 0
    turn = get_turn(n)
    pts_in_prev_spirals = (turn-2)**2  # -2 because spirals are all odd numbers
    pts_along_spiral = n - pts_in_prev_spirals
    pts_left = pts_along_spiral-1
    start_coord = int((turn-1)/2)
    pos = (start_coord, -(start_coord-1))

    direct = Direction.NORTH
    pts_moved = 0
    while pts_left > 0:
        pts_left -= 1
        pts_moved += 1
        pos = direct.move(pos)
        if (direct == Direction.NORTH and pts_moved >= turn-2) or pts_moved >= turn-1:
            pts_moved = 0
            direct = direct.turn_left()

    dist = manhattan_dist(pos, (0, 0))
    return dist


def spiral_distance_full(n: int) -> int:
    outer_turn = get_turn(n)
    mem = SpiralMemory(outer_turn)
    pos = mem.fill_to_value(n)

    dist = manhattan_dist(pos, (0, 0))
    return dist


def stress_test(n: int) -> int:
    outer_turn = get_turn(n)
    mem = SpiralMemory(outer_turn)
    output = mem.stress_test_to_val(n)
    return output


def spiral_distance(n: int, full_spiral: bool=False) -> int:
    if full_spiral:
        dist = spiral_distance_full(n)
    else:
        dist = spiral_distance_quick(n)
    return dist


def main() -> int:
    input_n = 368078
    dist = stress_test(input_n)
    #dist = spiral_distance(input_n, True)
    print(dist)
    return 0


if __name__ == '__main__':
    main()

