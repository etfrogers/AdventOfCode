import math
from collections import defaultdict, Counter
from typing import List, Tuple, Union
import numpy as np

from utils import Point
from intcode import IntCodeComputer


def main():
    comp = IntCodeComputer('input.txt', [])
    tiles = {}
    comp.execute()
    while comp.output_data:
        x, y, tile_id = comp.get_output(3)
        point = Point(x, y)
        tiles[point.tuple] = tile_id
    count = Counter(tiles.values())
    n_blocks = count[2]
    print(f'Number of blocks is {n_blocks}')


if __name__ == '__main__':
    main()
