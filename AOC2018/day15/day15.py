from enum import Enum
from typing import List

import numpy as np
from scipy.ndimage import measurements

UNITTYPE_DICT = {2: 'E', 3: 'G'}
UNITTYPE_DICT_INV = {item[1]: item[0] for item in UNITTYPE_DICT.items()}


class UnitType(Enum):
    ELF = 2
    GOBLIN = 3

    @staticmethod
    def to_string(value):
        return UNITTYPE_DICT[UnitType(value).value]

    @staticmethod
    def from_string(string):
        return UnitType(UNITTYPE_DICT_INV[string])


class Square:

    def __init__(self, position):
        self.position = position

    def distance_to(self, other):
        return np.sum(np.abs(self.position - other.position))

    @property
    def numpy_coord(self):
        return np.flipud(self.position)


NEARBY = [Square(np.array([-1, 0])),
          Square(np.array([1, 0])),
          Square(np.array([0, -1])),
          Square(np.array([0, 1])),
          ]


class Unit(Square):

    def __init__(self, type_, position):
        super().__init__(position)
        if type(type_) is str:
            type_ = UnitType.from_string(type_)
        elif type(type_) is int:
            type_ = UnitType(type_)
        self.type = type_

    def get_all_targets(self, fight):
        targets = []
        for unit in fight.units:
            if self.is_target(unit):
                targets.extend(unit.in_range_squares(fight.map))
        return in_reading_order(targets)

    def is_target(self, other):
        return self.type != other.type

    def filter_by_reachable(self, map_: np.ndarray, target_list: List[Square]):
        reachable = self.reachable_region(map_)
        return [target for target in target_list if reachable[tuple(target.numpy_coord)]]

    def find_target(self, fight):
        target_list = self.get_all_targets(fight)
        target_list = self.filter_by_reachable(fight.map, target_list)
        target_list.sort(key=lambda unit: self.distance_to(unit))
        nearby_targets = [target_list[0]]
        dist = self.distance_to(target_list[0])
        for unit in target_list:
            if self.distance_to(unit) > dist:
                break
            else:
                nearby_targets.append(unit)
        return in_reading_order(nearby_targets)[0]

    def in_range_squares(self, map_):
        return in_reading_order(
            [Square(self.position + pos.position) for pos in NEARBY
             if map_[tuple(self.numpy_coord + pos.numpy_coord)] == 0])

    def reachable_region(self, map_: np.ndarray):
        regions = map_.copy()
        regions[regions == 2] = 1  # remove elves
        regions[regions == 3] = 1  # remove goblins
        regions[tuple(self.numpy_coord)] = 0  # add back self
        regions = np.logical_not(regions).astype(int)
        measurements.label(regions, output=regions)
        return regions == regions[tuple(self.numpy_coord)]


class Fight:

    def __init__(self, input_map: str):
        array_str = input_map.replace('E', '2')
        array_str = array_str.replace('G', '3')
        array_str = array_str.replace('.', '0')
        array_str = array_str.replace('#', '1')
        array_list = [[int(v) for v in line] for line in array_str.split('\n')]
        self.map = np.array(array_list)
        self.cave = self.map.copy()
        self.cave[self.cave == 2] = 0
        self.cave[self.cave == 3] = 0
        elves = [Unit(UnitType.ELF, pos) for pos in np.transpose((self.map.transpose() == 2).nonzero())]
        goblins = [Unit(UnitType.GOBLIN, pos) for pos in np.transpose((self.map.transpose() == 3).nonzero())]
        self.units = elves + goblins

    def move_list(self):
        return in_reading_order(self.units)


def reading_order(position):
    return 10000 * position[1] + position[0]


def in_reading_order(lst):
    return sorted(lst, key=lambda unit: reading_order(unit.position))
