from copy import copy, deepcopy
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

import numpy as np
import networkx as nx
import string
from utils import array_to_string, string_to_array, Point, Directions


def is_wall(value):
    return value == '#'


def is_open(value):
    return is_key(value) or is_space(value) or is_entrance(value)


def is_key(value):
    return value in string.ascii_lowercase


def is_space(value):
    return value == '.'


def is_door(value):
    return value in string.ascii_uppercase


def is_entrance(value):
    return value == '@'


@dataclass
class Path:
    keys: List[str] = field(default_factory=list)
    route: List[Tuple[int, int]] = field(default_factory=list)

    def __len__(self):
        # subtract 1 as the route gives nodes, and we want edges.
        return len(self.route) - 1

    def append(self, keys: List[str], route: List[Tuple[int, int]]):
        self.keys.extend(keys)
        assert not self.route or route.pop(0) == self.route[-1]
        self.route.extend(route)

    def extend(self, new_path):
        self.append(new_path.keys, new_path.route)

    def __le__(self, other):
        return len(self) < len(other)


class Vault:

    def __init__(self, string_map):
        self.map: np.ndarray = string_to_array(string_map, dtype=str)
        # noinspection PyTypeChecker
        self.Graph: nx.Graph = None
        # noinspection PyTypeChecker
        self.current_position: Point = None
        self.keys: dict = {}
        self.doors: dict = {}
        self.graph, self.current_position, self.keys, self.doors = Vault.build_network(self.map)
        self.solve_stack = []
        self.found_paths: List[Path] = []
        self.path_steps = []
        self.steps = []

    def render(self) -> str:
        return array_to_string(self.map)

    @staticmethod
    def build_network(map_: np.ndarray) -> Tuple[nx.Graph, Point, dict, dict]:
        graph = nx.Graph()
        keys = {}
        doors = {}
        entrance = None
        for i in range(map_.shape[0]):
            for j in range(map_.shape[1]):
                point = Point(i, j)
                value = map_[point.tuple]
                if i == 0 or j == 0 or i == map_.shape[0] - 1 or j == map_.shape[1] - 1:
                    assert is_wall(value)
                    continue
                elif is_wall(value):
                    continue
                elif is_entrance(value):
                    entrance = copy(point)
                elif is_key(value):
                    keys[value] = point.tuple
                elif is_door(value):
                    doors[value] = point.tuple
                graph.add_node(point.tuple, value=value)
                if is_open(value):
                    Vault.add_routes_from_point(graph, map_, point)
        assert entrance is not None
        return graph, entrance, keys, doors

    @staticmethod
    def add_routes_from_point(graph, map_, point):
        directions = Directions()
        for direction in directions:
            neighbour = point + direction
            if is_open(map_[neighbour.tuple]):
                graph.add_edge(point.tuple, neighbour.tuple)

    def solve(self, test_mode: bool = False, path: Path = None):
        if path is None:
            self.found_paths = []
            path = Path()
        if not self.keys:
            self.found_paths.append(deepcopy(path))
            if test_mode:
                self.path_steps.append(deepcopy(self.steps))
            return
        poss_paths = [Path([key], shortest_path_or_none(self.graph, self.current_position.tuple, loc))
                      for key, loc in self.keys.items()]
        poss_paths = [path for path in poss_paths if path.route is not None]
        distances = [len(path) for path in poss_paths]
        distances, poss_paths = zip(*sorted(zip(distances, poss_paths)))

        for new_path in poss_paths:
            self.solve_stack.append((deepcopy(self), deepcopy(path)))

            path.extend(new_path)
            self.go_to_key(new_path.keys[0])
            # if self.keys:
            if test_mode:
                self.steps.append(self.render())
            self.solve(test_mode, path)
            old_state, path = self.solve_stack.pop()
            self.restore(old_state)
            # else:
            #     self.found_paths.append(path)

    def go_to_key(self, next_key):
        key_loc = self.keys[next_key]
        self.remove_key(next_key)
        self.set_current_position(Point(*key_loc))

    def restore(self, old_state):
        for field_name in ['map', 'Graph', 'current_position', 'keys', 'doors', 'steps']:
            value = getattr(old_state, field_name)
            self.__setattr__(field_name, value)

    def set_current_position(self, point):
        self.map[self.current_position.tuple] = '.'
        self.current_position = point
        self.map[point.tuple] = '@'

    def make_open(self, loc):
        self.graph.nodes[loc]['value'] = '.'
        self.map[loc] = '.'
        self.add_routes_from_point(self.graph, self.map, Point(*loc))

    def remove_key(self, key: str):
        loc = self.keys.pop(key)
        self.make_open(loc)
        try:
            self.open_door(key)
        except KeyError:
            pass

    def open_door(self, key: str):
        door = key.upper()
        loc = self.doors.pop(door)
        self.make_open(loc)

    def shortest_path(self):
        return min(self.path_lengths())

    def path_lengths(self):
        return [len(path) for path in self.found_paths]

    def get_steps_shortest_path(self):
        _, idx = min((val, idx) for (idx, val) in enumerate(self.path_lengths()))
        return self.path_steps[idx]


def shortest_path_or_none(*args, **kwargs):
    try:
        return nx.shortest_path(*args, **kwargs)
    except nx.NetworkXNoPath:
        return None


def main():
    with open('input.txt') as file:
        input_ = file.read()
    output = fft(input_, 100)
    print(output)
    print(f'First 8 chars: {output[:8]}')

    msg = get_fft_message(input_, 100)
    print(f'FFT message is: {msg}')


if __name__ == '__main__':
    main()
