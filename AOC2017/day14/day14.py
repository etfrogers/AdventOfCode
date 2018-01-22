import scipy.ndimage as ndimage
import numpy as np
from AOC2017.day10 import day10


def hash_to_bin(hash_string):
    bin_string = ''.join(['{0:0>4b}'.format(int(char, base=16)) for char in hash_string])
    return bin_string


def build_grid(grid_size, key):
    bits = []
    for i in range(0, grid_size):
        row_key = key + '-' + str(i)
        hash_string = day10.full_hash(256, row_key)
        bits.append(hash_to_bin(hash_string))
    return bits


def count_used_bits(bits):
    return sum([row.count('1') for row in bits])


def count_regions(bits):
    bit_array = np.array([[int(b) for b in row] for row in bits])
    _, nr_objects = ndimage.label(bit_array)
    return nr_objects


def main():
    key = 'jzgqcdpd'   # main input
    # key = 'flqrgnkx'   # test input
    grid_size = 128
    bits = build_grid(grid_size, key)
    print(count_regions(bits))


if __name__ == '__main__':
    main()
