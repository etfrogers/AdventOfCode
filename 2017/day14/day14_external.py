#! /usr/bin/env python3

# from https://github.com/jollyra/advent-of-code/tree/master/2017
from knot_hash_external import knot_hash
#from util import X, Y, neighbours4
from functools import partial


def find_regions(M):
    regions = []
    used_cells = find_used_cells(M)
    visited = set()
    unvisited = used_cells - visited
    while unvisited:
        p = unvisited.pop()
        region = explore_region(M, p)
        visited |= region
        regions.append(list(region))
        unvisited = used_cells - visited
    return regions


def explore_region(M, p):
    visited = set()
    horizon = set()
    horizon.add(p)
    while horizon:
        p = horizon.pop()
        visited.add(p)
        neighbours = filter(partial(is_in_bounds, len(M)), neighbours4(p))
        horizon |= {n for n in neighbours if M[Y(n)][X(n)] == '1' and n not in visited}
    return visited


def is_in_bounds(size, p):
    return 0 <= X(p) < size and 0 <= Y(p) < size


def find_used_cells(M):
    used_cells = set()
    for y in range(len(M)):
        for x in range(len(M)):
            if M[y][x] == '1':
                used_cells.add((x, y))
    return used_cells


def count_used_squares(M):
    return sum(1 for row in M for cell in row if cell == '1')


def decrypt_disk(string):
    key_strings = []
    for n in range(128):
        key_string = '{}-{}'.format(string, n)
        key_strings.append(key_string)
    print(key_strings)
    hashes = [knot_hash(s) for s in key_strings]
    print(hashes)
    bins = [hexstring_to_binary(h) for h in hashes]
    return bins


def hexstring_to_binary(hexs):
    ints = [int(x, 16) for x in hexs]
    bins = [format(i, 'b').zfill(4) for i in ints]
    binarystring = ''.join(bins)
    assert(len(binarystring) == 4 * len(hexs))
    return binarystring


if __name__ == '__main__':
    M = decrypt_disk('flqrgnkx')
    num_used_squares = count_used_squares(M)
    # assert(num_used_squares == 8230)
    # num_regions = len(find_regions(M))
    # assert(num_regions == 1103)
    # print('pass')
    # print('Memory used:', num_used_squares)
    # print('Regions:', num_regions)