import sys
import os
import numpy as np

rel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'day19')
sys.path.insert(0, rel_path)
# noinspection PyUnresolvedReferences
from day19 import Point
import day19


class Direction(day19.Direction):

    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    def __init__(self, *args):
        super().__init__(*args)

    def turn_left(self):
        curr = (self.x, self.y)
        if curr == self.NORTH:
            new = self.WEST
        elif curr == self.WEST:
            new = self.SOUTH
        elif curr == self.SOUTH:
            new = self.EAST
        elif curr == self.EAST:
            new = self.NORTH
        else:
            raise ValueError
        self.x, self.y = new

    def turn_right(self):
        curr = (self.x, self.y)
        if curr == self.NORTH:
            new = self.EAST
        elif curr == self.EAST:
            new = self.SOUTH
        elif curr == self.SOUTH:
            new = self.WEST
        elif curr == self.WEST:
            new = self.NORTH
        else:
            raise ValueError
        self.x, self.y = new


class VirusMap:

    CLEAN_CHAR = '.'
    INFECTED_CHAR = '#'
    CLEAN = 0
    INFECTED = 1
    EXPANSION = 5

    CHAR_MAPPING = {CLEAN_CHAR: CLEAN, INFECTED_CHAR: INFECTED}
    INT_MAPPING = {v: k for k,v in CHAR_MAPPING.items()}

    def __init__(self, map_string_list):
        self.map = self.parse_map_string(map_string_list)
        assert self.is_square()
        self.pos = Point(*self.get_centre())
        self.dir = Direction(*Direction.NORTH)
        self.infection_counter = 0

    def get_centre(self):
        return int((self.map.shape[0] - 1) / 2), int((self.map.shape[1] - 1) / 2)

    @property
    def shape(self):
        return self.map.shape

    @staticmethod
    def to_num(c):
        return VirusMap.CHAR_MAPPING[c]

    @staticmethod
    def parse_map_string(map_string_list):
        assert all([len(line) == len(map_string_list[0]) for line in map_string_list])
        data = [[VirusMap.to_num(c) for c in line] for line in map_string_list]
        return np.array(data)

    def __getitem__(self, item):
        if item.x < 0 or item.y < 0 or item.x >= self.map.shape[1] or item.y >= self.map.shape[0]:
            self.expand()
            item = item + Point(self.EXPANSION, self.EXPANSION)
        return self.map[item.y, item.x]

    def __setitem__(self, key, value):
        if key.x < 0 or key.y < 0 or key.x >= self.map.shape[1] or key.y >= self.map.shape[0]:
            self.expand()
            key = key + Point(self.EXPANSION, self.EXPANSION)
        self.map[key.y, key.x] = value

    def burst(self):
        status = self[self.pos]
        if status == self.INFECTED:
            self.dir.turn_right()
            self[self.pos] = self.CLEAN
        elif status == self.CLEAN:
            self.dir.turn_left()
            self[self.pos] = self.INFECTED
            self.infection_counter += 1
        else:
            raise ValueError
        self.pos += self.dir

    def do_bursts(self, n):
        self.infection_counter = 0
        for _ in range(n):
            self.burst()

    def expand(self):
        self.map = self.pad(self.map, (self.EXPANSION, self.EXPANSION))
        # shift point to maintain position relative to previous cells
        self.pos += Point(self.EXPANSION, self.EXPANSION)
        assert self.is_square()

    def is_square(self):
        return len(set(self.map.shape)) == 1

    @staticmethod
    def pad(array, pad_width):
        return np.pad(array, pad_width, mode='constant', constant_values=VirusMap.CLEAN)

    def __eq__(self, other):
        self_m = self.map.copy()
        other_m = other.map.copy()
        assert len(set(self_m.shape)) == 1
        assert len(set(other_m.shape)) == 1
        len_self = self_m.shape[0]
        len_other = other_m.shape[0]
        if len_self < len_other:
            padding = int((len_other - len_self) / 2)
            self_m = self.pad(self_m, (padding, padding))
        if len_self > len_other:
            padding = int((len_self - len_other) / 2)
            other_m = self.pad(other_m, (padding, padding))
        return np.all(self_m == other_m)


def main():
    with open('input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = VirusMap(map)
    print(vmap.map)
    vmap.do_bursts(10000)
    print(vmap.infection_counter)


if __name__ == '__main__':
    main()
