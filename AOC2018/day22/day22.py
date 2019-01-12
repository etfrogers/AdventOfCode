from collections import defaultdict
from typing import Tuple

import numpy as np


class KeyDefaultDict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


class Cave:
    EROSION_LEVELS = 20183

    def __init__(self, depth: int, target: Tuple[int, int], size: Tuple[int, int]=None):
        self.depth = depth
        self.target = target
        self.geologic_index = KeyDefaultDict(self.geologic_index_val)
        self.erosion_level = KeyDefaultDict(self.erosion_level_val)
        self.map = KeyDefaultDict(self.map_val)

    def map_val(self, coords):
        return self.type(self.erosion_level[coords])

    def erosion_level_val(self, coords):
        return np.mod(self.geologic_index[coords] + self.depth, self.EROSION_LEVELS)

    def geologic_index_val(self, coords):
        if coords == (0, 0):
            return 0
        elif coords == self.target:
            return 0
        elif coords[0] == 0:
            return coords[1] * 48271
        elif coords[1] == 0:
            return coords[0] * 16807
        else:
            return self.erosion_level[coords[0]-1, coords[1]] * self.erosion_level[coords[0], coords[1]-1]

    @staticmethod
    def type(erosion_level):
        return np.mod(erosion_level, 3)

    def map_lists(self, size=None):
        if size is None:
            size = self.target
        return [[self.map[(i, j)] for i in range(size[0]+1)] for j in range(size[1]+1)]

    def render(self, size=None):
        if size is None:
            size = self.target
        lists = self.map_lists(size)
        mapping = {0: '.', 1: '=', 2: '|'}
        lists = [[mapping[v] for v in lst] for lst in lists]
        lists[0][0] = 'M'
        lists[self.target[0]][self.target[1]] = 'T'
        return '\n'.join([''.join(i) for i in lists])

    def risk_level(self):
        return np.sum(np.array(self.map_lists()))


def main():
    depth = 3879
    target = (8, 713)
    cave = Cave(depth, target)
    print('Part 1: ', cave.risk_level())


if __name__ == '__main__':
    main()
