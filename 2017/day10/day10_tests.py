import day10
import numpy as np


def test_knot_hash():
    lengths = [3, 4, 1, 5]
    n = 5
    results, _, _ = day10.do_knot_hash(n, lengths)
    assert tuple(results) == (3, 4, 2, 1, 0)
    output = day10.calc_output(results)
    assert output == 12


def test_part1():
    lengths = np.loadtxt('input.txt', dtype=int, delimiter=',')
    n = 256
    results, _, _ = day10.do_knot_hash(n, lengths)
    output = day10.calc_output(results)
    assert output == 48705


def test_full_hash1():
    assert day10.full_hash(256, '') == 'a2582a3a0e66e6e86e3812dcb672a272'


def test_full_hash2():
    assert day10.full_hash(256, 'AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'


def test_full_hash3():
    assert day10.full_hash(256, '1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'


def test_full_hash4():
    assert day10.full_hash(256, '1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'


def test_part2():
    with open('input.txt', 'r') as file:
        lengths = file.read()
    lengths = lengths.strip()
    string = day10.full_hash(256, lengths)
    assert string == '1c46642b6f2bc21db2a2149d0aeeae5d'

