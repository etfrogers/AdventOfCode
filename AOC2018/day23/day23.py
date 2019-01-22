import re

import numpy as np

import AOC2018.day23.z3.z3 as z3


class Nanobot:
    PATTERN = re.compile(r'pos=<(-?[\d]+),(-?[\d]+),(-?[\d]+)>, r=(-?[\d]+)')

    def __init__(self, spec):
        matches = self.PATTERN.match(spec)
        self.pos = np.array([int(v) for v in matches.groups()[0:3]])
        self.range = int(matches.groups()[3])

    def dist_to(self, other):
        return distance(self.pos, other.pos)

    def in_range(self, bots):
        return [bot for bot in bots if self.dist_to(bot) <= self.range]


def get_strongest_bot(bots):
    return max(bots, key=lambda bot: bot.range)


def in_range_of_most(bots):
    x, y, z = z3.Ints('x y z')
    pt = np.array([x, y, z])
    in_range = [zdist(pt, bot.pos) < bot.range for bot in bots]
    z3.solve(in_range)
    pass


def zabs(x):
    return z3.If(x >= 0, x, -x)


def zdist(pos1, pos2):
    return zabs(pos1[0] - pos2[0]) + zabs(pos1[1] - pos2[1]) + zabs(pos1[2] - pos2[2])


def distance(pos1, pos2):
    return np.sum(np.abs(pos1 - pos2))
    # return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) + abs(pos1[2] - pos2[2])
    # return sum([abs(p1 - p2) for p1, p2 in zip(pos1, pos2)])



def main():
    with open('input.txt') as f:
        specs = f.readlines()
    bots = [Nanobot(spec) for spec in specs]
    bot = get_strongest_bot(bots)
    bots_in_range = bot.in_range(bots)
    print('Part 1: ', len(bots_in_range))


if __name__ == '__main__':
    main()
