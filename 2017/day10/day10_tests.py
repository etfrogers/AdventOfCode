import day10
import numpy as np


def test_knot_hash():
    lengths = [3, 4, 1, 5]
    n = 5
    results = day10.do_knot_hash(n, lengths)
    assert tuple(results) == (3, 4, 2, 1, 0)
    output = day10.calc_output(results)
    assert output == 12


def test_part1():
    lengths = np.loadtxt('input.txt', dtype=int)
    n = 256
    results = day10.do_knot_hash(n, lengths)
    output = day10.calc_output(results)
    assert output == 48705
