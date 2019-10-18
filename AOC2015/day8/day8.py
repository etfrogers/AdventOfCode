import itertools
from collections import namedtuple

import numpy as np


def parse_distances(specs):
    data = []
    for line in specs:
        ends, distance = line.split(' = ')
        data_point = namedtuple('Distance', ['distance', 'ends'])
        data_point.distance = int(distance)
        data_point.ends = set(ends.split(' to '))
        data.append(data_point)
    data_dict = {frozenset(d.ends): d.distance for d in data}
    return data, data_dict


def get_distance(route, data_dict):
    total_distance = 0
    for start, end in zip(route[:-1], route[1:]):
        total_distance += data_dict[frozenset((start, end))]
    return total_distance


def calculate_path(data, data_dict, get_max=False):
    all_points = set([item for d in data for item in d.ends])
    routes = itertools.permutations(all_points)
    distances = {get_distance(route, data_dict): route for route in routes}
    if get_max:
        tgt_distance = max(distances.keys())
    else:
        tgt_distance = min(distances.keys())
    return tgt_distance, distances[tgt_distance]


def main():
    with open('input.txt') as f:
        distances = f.readlines()
    data, data_dict = parse_distances(distances)
    distance, path = calculate_path(data, data_dict)
    print(f'Part 1: Minimum distance {distance}')

    distance, path = calculate_path(data, data_dict, get_max=True)
    print(f'Part 2: Maximum distance {distance}')


if __name__ == '__main__':
    main()
