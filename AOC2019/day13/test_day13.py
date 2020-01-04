from collections import Counter

import pytest

from AOC2019.day13.day13 import Game
from intcode import IntCodeComputer


def test_part1():
    comp = IntCodeComputer('input.txt', [])
    game = Game(comp)
    game.calc_new_frame()
    count = Counter(game.tiles.values())
    n_blocks = count[2]
    assert n_blocks == 173


def test_part2():
    comp = IntCodeComputer('input.txt', [])
    comp.instructions[0] = 2
    game = Game(comp)
    while not game.comp.finished:
        game.set_joystick()
        game.calc_new_frame()
    assert game.score == 8942
