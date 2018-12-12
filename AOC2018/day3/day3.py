from typing import List

import numpy as np
import re


class Claim:
    PATTERN = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)\n?')

    def __init__(self, claim_str):
        matches = self.PATTERN.match(claim_str)
        self.id, self.left, self.top, self.width, self.height = (int(g) for g in matches.groups())

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    def add_to_map(self, map_):
        map_slice = self.slice_map(map_)
        map_slice += 1

    def slice_map(self, map_):
        return map_[self.left:self.right, self.top:self.bottom]

    def is_uncontested_in_map(self, claim_map):
        map_slice = self.slice_map(claim_map)
        assert (map_slice == 0).sum() == 0
        return np.all(map_slice == 1)


def build_map(claims: List[Claim]):
    map_width = max([claim.right for claim in claims]) + 1
    map_height = max([claim.bottom for claim in claims]) + 1
    map_ = np.zeros((map_width, map_height))
    for claim in claims:
        claim.add_to_map(map_)
    return map_


def count_conflicts(map_):
    return (map_ > 1).sum()


def find_uncontested_claim(claims, claim_map):
    uncontested = [claim for claim in claims if claim.is_uncontested_in_map(claim_map)]
    assert len(uncontested) == 1
    return uncontested[0]


if __name__ == '__main__':
    with open('input.txt') as f:
        input = f.readlines()
    claims = [Claim(c) for c in input]
    claim_map = build_map(claims)
    conflicts = count_conflicts(claim_map)
    print(conflicts)

    uncontested = find_uncontested_claim(claims, claim_map)
    print(uncontested.id)
