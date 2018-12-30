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
        self._initial_state = initial_state.copy()
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

    def reset(self):
        self.layout = self._initial_state.copy()

    def frozen_layout(self):
        return tuple(self.layout.tolist())

    def get_total_resources(self, n):
        self.reset()
        i = 0
        resource_list = [self.total_resources]
        state_list = [self.frozen_layout()]
        while True:
            if i == n:
                return resource_list[-1]
            self.evolve()
            if self.frozen_layout() in state_list:
                break
            resource_list.append(self.total_resources)
            state_list.append(self.frozen_layout())
            i += 1
        # loop_end = i+1
        loop_start = state_list.index(self.frozen_layout())
        loop = resource_list[loop_start:]
        loop_length = len(loop)

        index = (n-loop_start) % loop_length
        return loop[index]


def main():
    with open('input.txt') as f:
        initial_state = f.read()
    area = Area(initial_state)
    area.evolve(10)
    print('Part 1: ', area.total_resources)

    # area = Area(initial_state)
    # for i in range(1000):
    #     area.evolve()
    #     print(i, ': ', area.total_resources)

    n = 1000000000
    area = Area(initial_state)
    print('Part 2: ', area.get_total_resources(n))


if __name__ == '__main__':
    main()
