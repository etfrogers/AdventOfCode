import numpy as np

from AOC2018.day23 import day23

test_input = '''pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1'''


def test1():
    bots = [day23.Nanobot(spec) for spec in test_input.split('\n')]
    bot = day23.get_strongest_bot(bots)
    assert np.all(np.array([0, 0, 0]) == bot.pos)
    assert bot.range == 4


def test2():
    bots = [day23.Nanobot(spec) for spec in test_input.split('\n')]
    bot = day23.get_strongest_bot(bots)
    bots_in_range = bot.in_range(bots)
    assert len(bots_in_range) == 7


def test_part1():
    with open('input.txt') as f:
        specs = f.readlines()
    bots = [day23.Nanobot(spec) for spec in specs]
    bot = day23.get_strongest_bot(bots)
    bots_in_range = bot.in_range(bots)
    assert len(bots_in_range) == 433


part2_test_input = '''pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5'''


def test_in_range_of_most():
    bots = [day23.Nanobot(spec) for spec in part2_test_input.split('\n')]
    point = day23.in_range_of_most(bots)
    assert np.array_equal(point, np.array([12, 12, 12]))


def test_in_range_of_most_and_dist():
    bots = [day23.Nanobot(spec) for spec in part2_test_input.split('\n')]
    point = day23.in_range_of_most(bots)
    assert day23.distance(point, np.array([0, 0, 0])) == 36


def test_part2():
    with open('input.txt') as f:
        specs = f.readlines()
    bots = [day23.Nanobot(spec) for spec in specs]

    point = day23.in_range_of_most(bots)
    assert day23.distance(point, np.array([0, 0, 0])) == 107272899
