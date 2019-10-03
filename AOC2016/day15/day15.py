import re
from collections import OrderedDict


class Discs(OrderedDict):
    SPEC_REG_EXP = re.compile(r'Disc #(\d) has (\d+) positions; at time=0, it is at position (\d+).')

    def parse_specs(self, specs):
        for spec in specs:
            label, n_positions, start_pos = self.parse_spec(spec)
            self[label] = Disc(n_positions, start_pos)

    @staticmethod
    def parse_spec(spec):
        matches = Discs.SPEC_REG_EXP.match(spec)
        return (int(v) for v in matches.groups())

    def find_path_start_time(self):
        start_time = 0
        # labels = self.keys()
        # discs = self.items()
        while True:
            positions = [(d.start_pos+label+start_time) % d.n_positions for label, d in self.items()]
            if all([p == 0 for p in positions]):
                return start_time
            start_time += 1


class Disc:
    def __init__(self, n_positions, start_pos):
        self.n_positions = n_positions
        self.start_pos = start_pos


def main():
    with open('input.txt') as file:
        specs = file.readlines()
    discs = Discs()
    discs.parse_specs(specs)

    start_time = discs.find_path_start_time()
    print('Part 1: time = ', start_time)

if __name__ == '__main__':
    main()