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
    cost = z3.Int('cost')
    pt = np.array([x, y, z])
    origin = np.array([0, 0, 0])
    in_range = [z3.If(zdist(pt, bot.pos) < bot.range, 1, 0) for bot in bots]
    # cost_expr = [z3.If(r, 1, 0) for r in in_range]
    opt = z3.Optimize()
    opt.add(cost == z3.Sum(in_range))
    opt.maximize(cost)
    opt.minimize(zdist(pt, origin))
    opt.check()
    print(opt.model())
    pass


def zabs(x):
    return z3.If(x >= 0, x, -x)


def zdist(pos1, pos2):
    pos2_ = pos2.tolist()
    return zabs(pos1[0] - pos2_[0]) + zabs(pos1[1] - pos2_[1]) + zabs(pos1[2] - pos2_[2])


def distance(pos1, pos2):
    return np.sum(np.abs(pos1 - pos2))


def main():
    with open('input.txt') as f:
        specs = f.readlines()
    bots = [Nanobot(spec) for spec in specs]
    bot = get_strongest_bot(bots)
    bots_in_range = bot.in_range(bots)
    print('Part 1: ', len(bots_in_range))


if __name__ == '__main__':
    main()
