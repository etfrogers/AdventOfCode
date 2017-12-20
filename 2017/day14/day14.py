import sys
sys.path.insert(0, r'C:\Users\Ed\Dropbox (Personal)\AOC\2017\day10')
# noinspection PyUnresolvedReferences
import day10


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


def main():
    key = 'jzgqcdpd'   # main input
    # key = 'flqrgnkx'   # test input
    grid_size = 128
    bits = build_grid(grid_size, key)
    print(count_used_bits(bits))


if __name__ == '__main__':
    main()
