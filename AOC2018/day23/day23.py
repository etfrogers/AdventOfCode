import re

import numpy as np


class Nanobot:
    PATTERN = re.compile(r'pos=<(-?[\d]+),(-?[\d]+),(-?[\d]+)>, r=(-?[\d]+)')

    def __init__(self, spec):
        matches = self.PATTERN.match(spec)
        self.pos = np.array([int(v) for v in matches.groups()[0:3]])
        self.range = int(matches.groups()[3])

    def dist_to(self, other):
        return np.sum(np.abs(self.pos - other.pos))

    def in_range(self, bots):
        return [bot for bot in bots if self.dist_to(bot) <= self.range]


def get_strongest_bot(bots):
    return max(bots, key=lambda bot: bot.range)


def main():
    with open('input.txt') as f:
        specs = f.readlines()
    bots = [Nanobot(spec) for spec in specs]
    bot = get_strongest_bot(bots)
    bots_in_range = bot.in_range(bots)
    print('Part 1: ', len(bots_in_range))


if __name__ == '__main__':
    main()
