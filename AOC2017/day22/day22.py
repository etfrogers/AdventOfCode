import collections

from utils import Point, DirectionsNP


class VirusMap:

    CLEAN = '.'
    INFECTED = '#'
    WEAKENED = 'W'
    FLAGGED = 'F'

    def __init__(self, map_string_list, evolved=False):
        self.map = self.parse_map_string(map_string_list)
        self.pos = Point(0, 0)
        self.dir = DirectionsNP.NORTH
        self.infection_counter = 0
        self.evolved = evolved

    @staticmethod
    def get_centre(string_list):
        assert all([len(line) == len(string_list[0]) for line in string_list])
        return int((len(string_list[0]) - 1) / 2), int((len(string_list) - 1) / 2)

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
        if self.evolved:
            if status == self.CLEAN:
                self.dir.turn_left()
                self[self.pos] = self.WEAKENED
            elif status == self.WEAKENED:
                self[self.pos] = self.INFECTED
                self.infection_counter += 1
            elif status == self.INFECTED:
                self.dir.turn_right()
                self[self.pos] = self.FLAGGED
            elif status == self.FLAGGED:
                self.dir.reverse()
                self[self.pos] = self.CLEAN
        else:
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
    vmap = VirusMap(map, evolved=True)
    print(vmap.map)
    vmap.do_bursts(10000000)
    print(vmap.infection_counter)


if __name__ == '__main__':
    main()
