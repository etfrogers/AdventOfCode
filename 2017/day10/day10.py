import numpy as np
import functools


def do_knot_hash(hash, lengths, position=0, skip_size=0):
    try:
        iter(hash)
    except TypeError:
        hash = np.array(range(0, hash))

    n = len(hash)
    for length in lengths:
        if length != 0:
            indexes = (np.array(list(range(0, length))) + position) % n
            hash[indexes] = np.flipud(hash[indexes])
        position = (position + length + skip_size) % n
        skip_size += 1
    return hash, position, skip_size


def calc_output(results):
    return results[0] * results[1]


def string_to_lengths(string):
    lengths = [ord(c) for c in string]
    return lengths


def sparse_to_dense(hash):
    hash = np.reshape(hash, (16, -1))
    dense_hash = []
    for line in hash:
        dense_hash.append(functools.reduce((lambda a, b: a ^ b), line))
    return dense_hash


def hash_to_string(dense_hash):
    list_of_chars_pairs = [hex(val)[2:] for val in dense_hash]
    list_of_chars_pairs = ['0'+c if len(c) == 1 else c for c in list_of_chars_pairs]
    return ''.join(list_of_chars_pairs)


def full_hash(n, string):
    lengths = string_to_lengths(string)
    suffix = [17, 31, 73, 47, 23]
    lengths = lengths + suffix

    hash = np.array(range(0, n))
    position = 0
    skip_size = 0
    for i in range(0, 64):
        hash, position, skip_size = do_knot_hash(hash, lengths, position, skip_size)

    dense_hash = sparse_to_dense(hash)
    str_hash = hash_to_string(dense_hash)
    return str_hash


def main():
    with open('input.txt', 'r') as file:
        lengths = file.read()
    lengths = lengths.strip()

    string = full_hash(256, lengths)
    print(string)


if __name__ == '__main__':
    main()
