import day22
import numpy as np


def string_to_pattern(string):
    return day22.VirusMap(string.split('\n'))


def test_burst_0():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = day22.VirusMap(map)
    vmap.do_bursts(0)
    string = '''.........
.........
.........
.....#...
...#.....
.........
.........
.........
.........'''
    assert string_to_pattern(string) == vmap


def test_burst_1():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = day22.VirusMap(map)
    vmap.do_bursts(1)
    string = '''.........
.........
.........
.....#...
...##....
.........
.........
.........
.........'''
    assert string_to_pattern(string) == vmap


def test_burst_2():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = day22.VirusMap(map)
    vmap.do_bursts(2)
    string = '''.........
.........
.........
.....#...
....#....
.........
.........
.........
.........'''
    assert string_to_pattern(string) == vmap


def test_burst7():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = day22.VirusMap(map)
    vmap.do_bursts(7)
    string = '''.........
.........
.........
..#..#...
..###....
.........
.........
.........
.........'''
    assert string_to_pattern(string) == vmap


def test_burst70():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = day22.VirusMap(map)
    vmap.do_bursts(70)
    string = '''.....##..
....#..#.
...#....#
..#.#...#
..#.#..#.
.....##..
.........
.........
.........'''
    assert string_to_pattern(string) == vmap


def test_count7():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = day22.VirusMap(map)
    vmap.do_bursts(7)
    assert vmap.infection_counter == 5


def test_count70():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = day22.VirusMap(map)
    vmap.do_bursts(70)
    assert vmap.infection_counter == 41


def test_count10000():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = day22.VirusMap(map)
    vmap.do_bursts(10000)
    assert vmap.infection_counter == 5587


def test_part1():
    with open('input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = day22.VirusMap(map)
    vmap.do_bursts(10000)
    assert vmap.infection_counter == 5305


def test_evolved_100():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = day22.VirusMap(map, evolved=True)
    vmap.do_bursts(100)
    assert vmap.infection_counter == 26


def test_evolved_10million():
    with open('test_input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = day22.VirusMap(map, evolved=True)
    vmap.do_bursts(10000000)
    assert vmap.infection_counter == 2511944


def test_part2():
    with open('input.txt', 'r') as file:
        map = file.readlines()
    map = [line.strip() for line in map]
    vmap = day22.VirusMap(map, evolved=True)
    vmap.do_bursts(10000000)
    assert vmap.infection_counter == 2511424
