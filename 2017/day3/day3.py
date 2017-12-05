import math
from typing import Tuple


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


def turn_left(dir_in: Tuple[int, int]) -> Tuple[int, int]:
    if dir_in == (0, 1):
        dir_out = (-1, 0)
    elif dir_in == (-1, 0):
        dir_out = (0, -1)
    elif dir_in == (0, -1):
        dir_out = (1, 0)
    elif dir_in == (1, 0):
        dir_out = (0, 1)
    else:
        raise ValueError

    return dir_out


def spiral_distance(n: int) -> int:
    if n == 1:
        return 0
    turn = get_turn(n)
    pts_in_prev_spirals = (turn-2)**2  # -2 because spirals are all odd numbers
    pts_along_spiral = n - pts_in_prev_spirals
    pts_left = pts_along_spiral-1
    start_coord = int((turn-1)/2)
    pos = (start_coord, -(start_coord-1))

    direct = (0, 1)
    pts_moved = 0
    while pts_left > 0:
        pts_left -= 1
        pts_moved += 1
        pos = add_pos(pos, direct)
        if (direct == (0, 1) and pts_moved >= turn-2) or pts_moved >= turn-1:
            pts_moved = 0
            direct = turn_left(direct)

    dist = manhattan_dist(pos, (0, 0))

    return dist


def main() -> int:
    input_n = 368078
    dist = spiral_distance(input_n)
    print(dist)
    return 0


if __name__ == '__main__':
    main()

