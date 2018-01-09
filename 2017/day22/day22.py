import sys
import os
import numpy as np
import collections

rel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'day19')
sys.path.insert(0, rel_path)
# noinspection PyUnresolvedReferences
import day19


class Point(day19.Point):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def tuple(self):
        return self.x, self.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


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
    CLEAN = CLEAN_CHAR
    INFECTED = INFECTED_CHAR

    CHAR_MAPPING = {CLEAN_CHAR: CLEAN, INFECTED_CHAR: INFECTED}
    INT_MAPPING = {v: k for k, v in CHAR_MAPPING.items()}

    def __init__(self, map_string_list):
        self.map = self.parse_map_string(map_string_list)
        self.pos = Point(0, 0)
        self.dir = Direction(*Direction.NORTH)
        self.infection_counter = 0

    @staticmethod
    def get_centre(string_list):
        assert all([len(line) == len(string_list[0]) for line in string_list])
        return int((len(string_list[0]) - 1) / 2), int((len(string_list) - 1) / 2)

    @staticmethod
    def to_num(c):
        return VirusMap.CHAR_MAPPING[c]

    @staticmethod
    def parse_map_string(map_string_list):
        centre = VirusMap.get_centre(map_string_list)
        new_map = collections.defaultdict(lambda: VirusMap.CLEAN)
        assert all([len(line) == len(map_string_list[0]) for line in map_string_list])
        for i, line in enumerate(map_string_list):
            for j, c in enumerate(line):
                if not c == VirusMap.CLEAN:
                    new_map[(j-centre[1], i-centre[0])] = c
        return new_map

    def __getitem__(self, item):
        return self.map[item.tuple]

    def __setitem__(self, key, value):
        self.map[key.tuple] = value

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

    def __eq__(self, other):
        self_m = {k: v for k, v in self.map.items() if not v == self.CLEAN}
        other_m = {k: v for k, v in other.map.items() if not v == self.CLEAN}
        unmatched_item = set(self_m.items()) ^ set(other_m.items())
        return len(unmatched_item) == 0


def main():
    with open('input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = VirusMap(map)
    print(vmap.map)
    vmap.do_bursts(1000000)
    print(vmap.infection_counter)




if __name__ == '__main__':
    main()
