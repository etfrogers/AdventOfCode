import hashlib
from collections import Counter

DOORS = 'UDLR'
OPEN_CHARS = {'b', 'c', 'd', 'e', 'f'}
TARGET = (3, 3)


def hash_chars(code):
    full_hash = hashlib.md5(code.encode('ascii')).hexdigest()
    return full_hash[0:4]


def is_open(char):
    return char in OPEN_CHARS


def find_open_doors(code):
    hash_ = hash_chars(code)
    return ''.join([d for c, d in zip(hash_, DOORS) if is_open(c)])


def stays_inside_walls(route):
    x_pos, y_pos = get_pos(route)
    return 0 <= x_pos <= 3 and 0 <= y_pos <= 3


def get_pos(route):
    counts = Counter(route)
    x_pos = counts['R'] - counts['L']
    y_pos = counts['D'] - counts['U']
    return x_pos, y_pos


def find_paths(passcode, route, all_routes):
    if route is None:
        route = ''
    if get_pos(route) == TARGET:
        all_routes.append(route)
        return ''
    possibilities = find_open_doors(passcode + route)
    for p in possibilities:
        candidate = route + p
        if stays_inside_walls(candidate):
            new_route = find_paths(passcode, candidate, all_routes)
            if new_route:
                return new_route
    return ''


def find_shortest_path(passcode):
    paths = []
    find_paths(passcode, '', paths)
    lengths = [len(path) for path in paths]
    min_length = min(lengths)
    shortest_path = [path for path in paths if len(path) == min_length]
    assert len(shortest_path) == 1
    return shortest_path[0]


def find_longest_path_length(passcode):
    paths = []
    find_paths(passcode, '', paths)
    lengths = [len(path) for path in paths]
    max_length = max(lengths)
    return max_length


def main():
    passcode = 'hijkl'
    passcode = 'ioramepc'
    path = find_shortest_path(passcode)
    print('Part 1: ', path)

    print('Part 2: ', find_longest_path_length(passcode))


if __name__ == '__main__':
    main()
