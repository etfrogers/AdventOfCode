#! /usr/bin/env python3

# from https://github.com/jollyra/advent-of-code/tree/master/2017
from functools import reduce


SALT = [17, 31, 73, 47, 23]
NUM_ROUNDS = 64
STANDARD_SIZE = 256
STANDARD_CHUNK_SIZE = 16


def knot_hash(ascii_str):
    dense_hash = dense_knot_knot_hash(ascii_str)
    hexstring = to_hexstring(dense_hash)
    return hexstring


def dense_knot_knot_hash(ascii_str):
    sparse_hash = sparse_knot_knot_hash(ascii_str)
    seqs = chunks(STANDARD_CHUNK_SIZE, sparse_hash)
    dense_hash = [reduce(lambda x, y: x ^ y, seq) for seq in seqs]
    return dense_hash


def sparse_knot_knot_hash(ascii_str):
    lengths = to_ascii_codes(ascii_str) + SALT
    seq = list(range(STANDARD_SIZE))
    current_pos = 0
    skip_size = 0
    for _ in range(NUM_ROUNDS):
        seq, current_pos, skip_size = knot_hash_round(seq, lengths, current_pos, skip_size)
    return seq


def knot_hash_round(seq, lengths, pos, skip_size):
    size = len(seq)
    for length in lengths:
        sublist = read_wrapping_sublist(seq, length, pos)
        write_wrapping_sublist(seq, sublist[::-1], pos)
        pos = (pos + length + skip_size) % size
        skip_size += 1
    return (seq, pos, skip_size)


def part1(seq, lengths, pos, skip_size):
    seq, pos, skip_size = knot_hash_round(seq, lengths, pos, skip_size)
    return seq[0] * seq[1]


def read_wrapping_sublist(seq, length, pos):
    j = pos
    sublist = []
    while j < pos + length:
        sublist.append(seq[j % len(seq)])
        j += 1
    return sublist


def write_wrapping_sublist(seq, sublist, pos):
    for k in range(len(sublist)):
        seq[pos % len(seq)] = sublist[k]
        pos += 1


def to_ascii_codes(seq):
    codes = bytearray(seq, 'ascii')
    return list(map(int, codes))


def chunks(chunk_size, seq):
    return [seq[i:i + chunk_size] for i in range(0, len(seq), chunk_size)]


def to_hexstring(dense_hash):
    hex_seq = ['{0:x}'.format(ascii_code).zfill(2) for ascii_code in dense_hash]
    return ''.join(hex_seq)


if __name__ == '__main__':
    seq5 = list(range(5))
    assert(part1(seq5, [3, 4, 1, 5], 0, 0) == 12)
    seq256 = list(range(STANDARD_SIZE))
    input_lengths = [157, 222, 1, 2, 177, 254, 0, 228, 159, 140, 249, 187, 255, 51, 76, 30]
    assert(part1(seq256, input_lengths, 0, 0) == 62238)

    assert(knot_hash('') == 'a2582a3a0e66e6e86e3812dcb672a272')
    assert(knot_hash('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd')
    assert(knot_hash('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d')
    assert(knot_hash('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e')
    aoc_input_str = '157,222,1,2,177,254,0,228,159,140,249,187,255,51,76,30'
    assert(knot_hash(aoc_input_str) == '2b0c9cc0449507a0db3babd57ad9e8d8')
    print(knot_hash('flqrgnkx-0'))
    print('pass')