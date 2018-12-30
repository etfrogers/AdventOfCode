from enum import Enum

import numpy as np

from AOC2018.day18.cellular_automata.automata.automata import Automata
from AOC2018.day18.cellular_automata.automata.rule import Rule, MultiRule

LANDTYPE_DICT = {0: '.', 1: '|', 2: '#'}
LANDTYPE_DICT_INV = {item[1]: item[0] for item in LANDTYPE_DICT.items()}


class LandType(Enum):
    OPEN = 0
    TREES = 1
    LUMBERYARD = 2

    @staticmethod
    def to_string(value):
        return LANDTYPE_DICT[LandType(value).value]

    @staticmethod
    def from_string(string):
        return LandType(LANDTYPE_DICT_INV[string])


class Area(Automata):
    def __init__(self, initial_state_str):
        initial_state_list = [[LandType.from_string(c).value for c in line] for line in initial_state_str.split('\n')]
        initial_state = np.array(initial_state_list)
        super().__init__(initial_state.shape, [t.value for t in LandType])
        self.layout = initial_state
        self.add_rule(Rule(LandType.OPEN.value, LandType.TREES.value, LandType.TREES.value, (3, 8)))
        self.add_rule(Rule(LandType.TREES.value, LandType.LUMBERYARD.value, LandType.LUMBERYARD.value, (3, 8)))
        self.add_rule(MultiRule((LandType.LUMBERYARD.value, LandType.LUMBERYARD.value),
                                LandType.OPEN.value,
                                (LandType.LUMBERYARD.value, LandType.TREES.value),
                                ((0, 0), (0, 0)), combine_function=np.logical_or))

    def render(self):
        string_list = [[LandType.to_string(v) for v in line] for line in self.layout.tolist()]
        return '\n'.join([''.join(line) for line in string_list])

    @property
    def total_resources(self):
        n_trees = np.sum(self.layout == LandType.TREES.value)
        n_lumberyards = np.sum(self.layout == LandType.LUMBERYARD.value)
        return n_trees * n_lumberyards


def main():
    with open('input.txt') as f:
        initial_state = f.read()
    area = Area(initial_state)
    area.evolve(10)
    print('Part 1: ', area.total_resources)


if __name__ == '__main__':
    main()
