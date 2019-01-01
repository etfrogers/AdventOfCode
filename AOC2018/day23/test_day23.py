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
