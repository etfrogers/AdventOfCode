import math
from typing import Tuple
from enum import Enum


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
        pos = add_pos(pos, direct.value)
        if (direct == Direction.NORTH and pts_moved >= turn-2) or pts_moved >= turn-1:
            pts_moved = 0
            direct = direct.turn_left()

    dist = manhattan_dist(pos, (0, 0))

    return dist


def spiral_distance_full(n: int) -> int:
    return 0


def spiral_distance(n: int, full_spiral: bool=False) -> int:
    if full_spiral:
        dist = spiral_distance_full(n)
    else:
        dist = spiral_distance_quick(n)
    return dist


def main() -> int:
    input_n = 368078
    dist = spiral_distance(input_n)
    print(dist)
    return 0


if __name__ == '__main__':
    main()

