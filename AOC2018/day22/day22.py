from enum import Enum
from heapq import heappop, heappush
from typing import Tuple

import numpy as np

from utils import KeyDefaultDict


class Equipment(Enum):
    NEITHER = 0
    TORCH = 1
    CLIMBING_EQUIPMENT = 2

    def __lt__(self, other):
        return self.value < other.value


class CaveType(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2


class Cave:
    EROSION_LEVELS = 20183

    def __init__(self, depth: int, target: Tuple[int, int]):
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
        return CaveType(erosion_level % 3)

    def map_lists(self, size=None):
        if size is None:
            size = self.target
        return [[self.map[(i, j)] for i in range(size[0]+1)] for j in range(size[1]+1)]

    def render(self, size=None):
        if size is None:
            size = self.target
        lists = self.map_lists(size)
        mapping = {CaveType.ROCKY: '.',
                   CaveType.WET: '=',
                   CaveType.NARROW: '|'}
        lists = [[mapping[v] for v in lst] for lst in lists]
        lists[0][0] = 'M'
        lists[self.target[0]][self.target[1]] = 'T'
        return '\n'.join([''.join(i) for i in lists])

    def risk_level(self):
        return sum([item.value for sublist in self.map_lists() for item in sublist])

    def time_to_target(self):
        neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        target = self.target
        queue = []
        heappush(queue, (0, (0, 0), Equipment.TORCH))
        visited_nodes = {((0, 0), Equipment.TORCH): 0}

        while queue:
            # min_time = min_time_to(tree, target)
            # if min_time is not None and all([l > min_time for l in leaf_times(tree)]):
            #     break
            # print(RenderTree(tree, AsciiStyle()))

            old_time, old_pos, old_equipment = heappop(queue)
            curr_type = self.map[old_pos]
            for dir_ in neighbours:
                new_pos = (old_pos[0] + dir_[0], old_pos[1] + dir_[1])
                if any([v < 0 for v in new_pos]):
                    continue
                new_type = self.map[new_pos]

                transit_time, new_equipment = calculate_transit(old_equipment, curr_type, new_type)
                new_time = old_time + transit_time
                if new_pos == target and new_equipment != Equipment.TORCH:
                    new_time += 7
                    new_equipment = Equipment.TORCH
                # temp_node = anytree.AnyNode(coords=new_pos, equipment=new_equipment, time=new_time)
                new_key = (new_pos, new_equipment)
                # existing_node = equivalent_node(tree, new_pos, new_equipment) # if key in visited_nodes else None
                # visited_nodes.add(key)

                if new_time < visited_nodes.get(new_key, float('inf')) and new_time < visited_nodes.get((target, Equipment.TORCH), float('inf')):
                    heappush(queue, (new_time, new_pos, new_equipment))
                    visited_nodes[new_key] = new_time
        return visited_nodes[(target, Equipment.TORCH)]


def calculate_transit(curr_equipment, curr_type, new_type):
    move_time = 1
    switch_time = 8
    if new_type == CaveType.ROCKY:
        if curr_equipment in (Equipment.TORCH, Equipment.CLIMBING_EQUIPMENT):
            transit_time = move_time
        else:
            transit_time = switch_time
            if curr_type == CaveType.WET:
                curr_equipment = Equipment.CLIMBING_EQUIPMENT
            elif curr_type == CaveType.NARROW:
                curr_equipment = Equipment.TORCH
            else:
                raise NotImplemented
    elif new_type == CaveType.WET:
        if curr_equipment in (Equipment.NEITHER, Equipment.CLIMBING_EQUIPMENT):
            transit_time = move_time
        else:
            transit_time = switch_time
            if curr_type == CaveType.ROCKY:
                curr_equipment = Equipment.CLIMBING_EQUIPMENT
            elif curr_type == CaveType.NARROW:
                curr_equipment = Equipment.NEITHER
            else:
                raise NotImplemented
    elif new_type == CaveType.NARROW:
        if curr_equipment in (Equipment.NEITHER, Equipment.TORCH):
            transit_time = move_time
        else:
            transit_time = switch_time
            if curr_type == CaveType.ROCKY:
                curr_equipment = Equipment.TORCH
            elif curr_type == CaveType.WET:
                curr_equipment = Equipment.NEITHER
            else:
                raise NotImplemented
    else:
        raise NotImplemented
    return transit_time, curr_equipment


# def get_leaves(tree: anytree.AnyNode):
#     return anytree.findall(tree, filter_=lambda node: node.is_leaf)
#
#
# def leaf_times(tree):
#     return [node.time for node in get_leaves(tree)]
#
#
# def equivalent_node(tree, coords, equipment):
#     return anytree.find(tree, lambda node: node.coords == coords and node.equipment == equipment)
#
#
# def min_time_to(tree: anytree.AnyNode, coords: Tuple[int, int]):
#     target_paths = anytree.findall_by_attr(tree, value=coords, name='coords')
#     if target_paths:
#         return min([node.time for node in target_paths])
#     else:
#         return None
#
#
# def flip(a):
#     return a[1], a[0]


def main():
    depth = 3879
    target = (8, 713)
    cave = Cave(depth, target)
    print('Part 1: ', cave.risk_level())

    print('Part 2: ', cave.time_to_target())


if __name__ == '__main__':
    main()
