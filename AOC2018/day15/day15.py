from enum import Enum
from typing import List

import numpy as np
from scipy.ndimage import measurements, binary_dilation

UNITTYPE_DICT = {2: 'E', 3: 'G'}
UNITTYPE_DICT_INV = {item[1]: item[0] for item in UNITTYPE_DICT.items()}


class UnitType(Enum):
    ELF = 2
    GOBLIN = 3

    def to_string(self):
        return UNITTYPE_DICT[UnitType(self).value]

    @staticmethod
    def from_string(string):
        return UnitType(UNITTYPE_DICT_INV[string])


class Square:

    def __init__(self, position):
        self.position = position

    def __eq__(self, other):
        return np.array_equal(self.position, other.position)

    def __add__(self, other):
        return Square(self.position + other.position)

    @property
    def numpy_coord(self):
        return tuple(np.flipud(self.position))

    def distance_map(self, map_):
        SENTINEL = -1
        walls = Fight.get_walls_from_map(map_)
        elves = Fight.get_elves_from_map(map_)
        goblins = Fight.get_goblins_from_map(map_)
        units = np.logical_or(elves, goblins)
        blocks = np.logical_or(walls, units)

        max_dist = map_.size + 1
        dists = np.full_like(map_, SENTINEL)
        dists[self.numpy_coord] = 0  # by definition! can get overwritten above

        img = np.zeros_like(dists)
        img[self.numpy_coord] = 1
        dist = 1
        reachable_region = self.reachable_region(map_)
        while not np.all(np.logical_or.reduce((dists >= 0, np.logical_not(reachable_region), walls))):
            last_img = img.copy()
            img = binary_dilation(img).astype(int)
            dists[np.logical_and(dists == SENTINEL, img != last_img)] = dist
            img[blocks] = 0
            img[self.numpy_coord] = 1
            dist += 1
        dists[np.logical_or(walls, np.logical_not(reachable_region))] = max_dist
        dists[self.numpy_coord] = 0  # by definition! can get overwritten above
        return dists

    def reachable_region(self, map_: np.ndarray):
        regions = map_.copy()
        elves = regions == UnitType.ELF.value
        goblins = regions == UnitType.GOBLIN.value
        regions[elves] = 1  # remove elves
        regions[goblins] = 1  # remove goblins
        regions[self.numpy_coord] = 0  # add back self
        regions = np.logical_not(regions).astype(int)
        measurements.label(regions, output=regions)
        own_region: np.ndarray = regions == regions[self.numpy_coord]
        # add back reachable units
        units = np.logical_or(elves, goblins)
        adjacent = binary_dilation(own_region)
        units_adjacent = np.logical_and(units, adjacent)
        own_region[units_adjacent] = True
        return own_region

    def __str__(self):
        return f'({self.position[0]}, {self.position[1]})'

    def __repr__(self):
        return self.__str__()


NEARBY = [Square(np.array([0, -1])),  # these should be in reading order
          Square(np.array([-1, 0])),
          Square(np.array([1, 0])),
          Square(np.array([0, 1])),
          ]
NO_MOVEMENT = Square(np.array([0, 0]))


class Unit(Square):
    BASE_HIT_POINTS = 200
    BASE_ATTACK_POWER = 3

    def __init__(self, type_, position):
        super().__init__(position)
        if type(type_) is str:
            type_ = UnitType.from_string(type_)
        elif type(type_) is int:
            type_ = UnitType(type_)
        self.type = type_
        self._hit_points = Unit.BASE_HIT_POINTS
        self.attack_power = Unit.BASE_ATTACK_POWER

    @property
    def hit_points(self):
        return self._hit_points

    @hit_points.setter
    def hit_points(self, value):
        self._hit_points = value
        if self._hit_points < 0:
            self.type = None

    def __eq__(self, other):
        return self.type == other.type \
                and self.hit_points == other.hit_points \
                and self.attack_power == other.attack_power \
                and Square.__eq__(self, other)

    def get_all_targets(self, fight, distance_map):
        targets = []
        found_target_unit = False
        for unit in fight.units:
            if self.is_target(unit):
                found_target_unit = True
                if distance_map[unit.numpy_coord] <= 1:
                    # if already next to a target unit, add own position (which should then be nearest target), as a
                    # movement target
                    targets.append(Square(self.position))
                targets.extend(unit.in_range_squares(fight.map))
        return in_reading_order(targets) if found_target_unit else None

    def is_target(self, other):
        return self.type != other.type

    def filter_by_reachable(self, map_: np.ndarray, target_list: List[Square]):
        reachable = self.reachable_region(map_)
        return [target for target in target_list
                if reachable[target.numpy_coord] and
                (map_[target.numpy_coord] == 0 or np.array_equal(self.position, target.position))]

    def find_target(self, fight, distance_map):
        target_list = self.get_all_targets(fight, distance_map)
        if target_list is None:
            # no target UNITS found
            return None
        target_list = self.filter_by_reachable(fight.map, target_list)
        target_list.sort(key=lambda unit_: distance_map[unit_.numpy_coord])
        if not target_list:
            # no target SQUARES found (i.e. all enemy units are surrounded)
            return []
        nearby_targets = [target_list[0]]
        dist = distance_map[target_list[0].numpy_coord]
        if dist == 0:
            return Square(self.position)
        for unit in target_list[1:]:
            if distance_map[unit.numpy_coord] > dist:
                break
            else:
                nearby_targets.append(unit)
        return in_reading_order(nearby_targets)[0]

    def in_range_squares(self, map_):
        return [Square(self.position + pos.position) for pos in NEARBY if map_[(self + pos).numpy_coord] == 0]

    def move_in(self, fight):
        distance_map = self.distance_map(fight.map)
        target = self.find_target(fight, distance_map)
        if target is None:
            raise StopIteration
        elif not target:
            return
        direction = self.path_to(fight, target)
        fight.map[self.numpy_coord] = 0
        self.position += direction.position
        fight.map[self.numpy_coord] = self.type.value

    def path_to(self, fight, target: Square):
        if np.array_equal(self.position, target.position):
            return NO_MOVEMENT
        all_dists = target.distance_map(fight.map)
        dists = [all_dists[(self + pos).numpy_coord] if fight.map[(self+pos).numpy_coord] == 0 else np.amax(all_dists)
                 for pos in NEARBY]
        # index returns first occurrence, but that is ok because NEARBY is in reading order
        return NEARBY[dists.index(min(dists))]

    def attack_in(self, fight):
        targets = [fight.unit_at_pos((self+pos).position) for pos in NEARBY]
        targets = [t for t in targets if t is not None and self.is_target(t)]
        if targets:
            hp = [t.hit_points for t in targets]
            # index returns first occurrence, but that is ok because NEARBY is in reading order
            selected_target = targets[hp.index(min(hp))]
            selected_target.hit_points -= self.attack_power

    def __str__(self):
        return f'{self.type.to_string()}, ({self.position[0]}, {self.position[1]}): {self.hit_points}HP'

    def __repr__(self):
        return self.__str__()


class Fight:

    def __init__(self, input_map: str):
        self.completed_rounds = 0
        array_str = input_map.replace('E', '2')
        array_str = array_str.replace('G', '3')
        array_str = array_str.replace('.', '0')
        array_str = array_str.replace('#', '1')
        array_list = [[int(v) for v in line] for line in array_str.split('\n')]
        self.map: np.ndarray = np.array(array_list)
        x = np.arange(self.map.shape[1])
        y = np.arange(self.map.shape[0])
        self.x, self.y = np.meshgrid(x, y)
        elves = [Unit(UnitType.ELF, pos) for pos in np.transpose((self.map.transpose() == 2).nonzero())]
        goblins = [Unit(UnitType.GOBLIN, pos) for pos in np.transpose((self.map.transpose() == 3).nonzero())]
        self.units = elves + goblins

    def __eq__(self, other):
        return np.array_equal(self.map, other.map) and \
            all([a == b for a, b in zip(in_reading_order(self.units), in_reading_order(other.units))])

    @property
    def walls(self):
        return self.get_walls_from_map(self.map)

    @staticmethod
    def get_walls_from_map(map_):
        walls = map_.copy()
        walls[walls == UnitType.ELF.value] = 0
        walls[walls == UnitType.GOBLIN.value] = 0
        return walls

    @property
    def elves(self):
        return self.get_elves_from_map(self.map)

    @staticmethod
    def get_elves_from_map(map_):
        return (map_ == UnitType.ELF.value).astype(int)

    @property
    def goblins(self):
        return self.get_goblins_from_map(self.map)

    @staticmethod
    def get_goblins_from_map(map_):
        return (map_ == UnitType.GOBLIN.value).astype(int)

    def move_list(self):
        return in_reading_order(self.units)

    def do_round(self):
        for unit in self.move_list():
            if unit.type is None:
                # skip dead units. Needed because move_list is evaluated at start of loop, so cleanp only takes
                # effect on next round
                continue
            unit.move_in(self)
            unit.attack_in(self)
            self.cleanup_dead_units()

    def evolve(self, n_rounds: int=0):
        while n_rounds < 1 or self.completed_rounds < n_rounds:
            try:
                self.do_round()
            except StopIteration:
                return
            self.completed_rounds += 1

    def unit_at_pos(self, position):
        for unit in self.units:
            if np.array_equal(unit.position, position):
                return unit
        return None

    def cleanup_dead_units(self):
        for unit in self.units:
            if unit.type is None:
                self.map[unit.numpy_coord] = 0
        self.units = [unit for unit in self.units if unit.type is not None]

    def outcome(self):
        return self.completed_rounds * sum(unit.hit_points for unit in self.move_list())


def reading_order(position):
    return 10000 * position[1] + position[0]


def in_reading_order(lst):
    return sorted(lst, key=lambda unit: reading_order(unit.position))


def main():
    with open('input.txt') as f:
        initial_map = f.read()
    fight = Fight(initial_map)
    fight.evolve()
    print('Part 1: ', fight.outcome())


if __name__ == '__main__':
    main()

