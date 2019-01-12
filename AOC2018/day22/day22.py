from typing import Tuple

import numpy as np


class DynamicCachedArray:
    def __init__(self, generator: callable, shape=(1,1)):
        self.generator = generator
        self._values = np.full(shape, np.nan)

    def __getitem__(self, item):
        assert len(item) == 2
        assert all(i is not None for i in item)
        assert all(i > 0 for i in item)
        # try:
        val = self._values[item]
        # except:


class Cave:
    EROSION_LEVELS = 20183

    def __init__(self, depth: int, target: Tuple[int, int], size: Tuple[int, int]=None):
        self.depth = depth
        self.target = target
        self.size = size if size is not None else target
        self.x = np.arange(self.size[0])
        self.y = np.arange(self.size[1])
        # self.x, self.y = np.meshgrid(x, y)

    def build_map(self):
        return self.type(self.erosion_level())

    def erosion_level(self):
        return np.mod(self.geologic_index() + self.depth, self.EROSION_LEVELS)

    def geologic_index(self):
        gi = np.zeros(self.size, dtype=int)
        # (0,0) = 0 implicitly
        gi[1:, 0] = self.x[1:] * 16807
        gi[0, 1:] = self.y[1:] * 48271

        for i in range(1, max(self.size)):
            for j in range(i, self.size[0]):
                gi[i, j] = gi[i-1, j] * gi[i, j-1]
            for j in range(i, self.size[1]):
                gi[j, i] = gi[j-1, i] * gi[j, i-1]
        return gi

    @staticmethod
    def type(erosion_level):
        return np.mod(erosion_level, 3)

    @property
    def map(self):
        return self.build_map()

    @property
    def risk_level(self):
        return np.sum(self.map[:self.target[0], :self.target[1]])