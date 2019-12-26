import numpy as np
import pytest

from AOC2017.day22.day22 import VirusMap

cases = [(0, '''.........
.........
.........
.....#...
...#.....
.........
.........
.........
.........'''),
         (1, '''.........
.........
.........
.....#...
...##....
.........
.........
.........
.........'''),
         (2, '''.........
.........
.........
.....#...
....#....
.........
.........
.........
.........'''),
         (7, '''.........
.........
.........
..#..#...
..###....
.........
.........
.........
.........'''),
         (70, '''.....##..
....#..#.
...#....#
..#.#...#
..#.#..#.
.....##..
.........
.........
.........''')]


def string_to_pattern(string):
    return VirusMap(string.split('\n'))


@pytest.mark.parametrize('n, string', cases)
def test_burst(n, string):
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = VirusMap(map)
    vmap.do_bursts(n)
    assert string_to_pattern(string) == vmap


def test_count7():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = VirusMap(map)
    vmap.do_bursts(7)
    assert vmap.infection_counter == 5


def test_count70():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = VirusMap(map)
    vmap.do_bursts(70)
    assert vmap.infection_counter == 41


def test_count10000():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = VirusMap(map)
    vmap.do_bursts(10000)
    assert vmap.infection_counter == 5587


def test_part1():
    with open('input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = VirusMap(map)
    vmap.do_bursts(10000)
    assert vmap.infection_counter == 5305


def test_evolved_100():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = VirusMap(map, evolved=True)
    vmap.do_bursts(100)
    assert vmap.infection_counter == 26


def test_evolved_10million():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = VirusMap(map, evolved=True)
    vmap.do_bursts(10000000)
    assert vmap.infection_counter == 2511944


def test_part2():
    with open('input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = VirusMap(map, evolved=True)
    vmap.do_bursts(10000000)
    assert vmap.infection_counter == 2511424
