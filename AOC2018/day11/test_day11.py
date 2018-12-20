from AOC2018.day11 import day11
import numpy as np

def test1():
    rack = day11.Rack(8)
    assert rack[3, 5] == 4


def test2():
    rack = day11.Rack(8)
    assert rack[3, 5] == 4


def test3():
    rack = day11.Rack(8)
    assert rack[3, 5] == 4


def test4():
    rack = day11.Rack(8)
    assert rack[3, 5] == 4


def test5():
    rack = day11.Rack(18)
    assert rack.best_region() == ((33, 45), 29)


def test6():
    rack = day11.Rack(42)
    assert rack.best_region() == ((21, 61), 30)


def test_part_2_1():
    rack = day11.Rack(18)
    assert rack.best_region_scan_size() == (90, 269, 16)


def test_part_2_2():
    rack = day11.Rack(42)
    assert rack.best_region_scan_size() == (232, 251, 12)


def test_part1():
    rack = day11.Rack(3999)
    assert rack.best_region()[0] == (21, 77)


def test_part2():
    rack = day11.Rack(3999)
    assert rack.best_region_scan_size() == (224, 222, 27)
