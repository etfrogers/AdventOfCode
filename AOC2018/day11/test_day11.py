from AOC2018.day11 import day11


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
    assert rack.best_region() == (33, 45)


def test6():
    rack = day11.Rack(42)
    assert rack.best_region() == (21, 61)
