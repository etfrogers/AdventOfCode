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

    def time_to_target(self):
        neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        target = self.target
        size = tuple(np.round(np.array(target)*1.5).astype(int))
        times = np.full(size, np.nan)
        equipment = np.full_like(times, np.nan)  # 0 neither, 1 torch, 2 climbing
        times[0, 0] = 0
        equipment[0, 0] = 1  # torch
        for i in range(sum(size)):
            for x in range(i+1):
                y = i - x
                old_pos = (x, y)
                curr_type = self.map[old_pos]
                for dir_ in neighbours:
                    new_pos = (x + dir_[0], y + dir_[1])
                    if any([v < 0 for v in new_pos]):
                        continue
                    try:
                        curr_equipment = equipment[flip(old_pos)]
                    except IndexError:
                        continue
                    new_type = self.map[new_pos]

                    if new_type == 0:  # rocky
                        if curr_equipment in (1, 2):
                            transit_time = 1
                        else:
                            transit_time = 8
                            if curr_type == 1:
                                curr_equipment = 2
                            elif curr_type == 2:
                                curr_equipment = 1
                            else:
                                raise NotImplemented
                    elif new_type == 1:
                        if curr_equipment in (0, 2):
                            transit_time = 1
                        else:
                            transit_time = 8
                            if curr_type == 0:
                                curr_equipment = 2
                            elif curr_type == 2:
                                curr_equipment = 0
                            else:
                                raise NotImplemented
                    elif new_type == 2:
                        if curr_equipment in (0, 1):
                            transit_time = 1
                        else:
                            transit_time = 8
                            if curr_type == 0:
                                curr_equipment = 1
                            elif curr_type == 1:
                                curr_equipment = 0
                            else:
                                raise NotImplemented
                    else:
                        raise NotImplemented
                    try:
                        new_time = times[flip(old_pos)] + transit_time
                        if np.isnan(times[flip(new_pos)]) or new_time < times[flip(new_pos)]:
                            times[flip(new_pos)] = new_time
                            equipment[flip(new_pos)] = curr_equipment
                    except IndexError:
                        pass
        return times[flip(self.target)]


def flip(a):
    return a[1], a[0]


def main():
    depth = 3879
    target = (8, 713)
    cave = Cave(depth, target)
    print('Part 1: ', cave.risk_level())


if __name__ == '__main__':
    main()
