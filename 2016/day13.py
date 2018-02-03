import numpy as np
from typing import Tuple
from scipy.ndimage.morphology import binary_dilation


class Office:
    def __init__(self, size, salt):
        self.layout = np.zeros(size, dtype=int)
        self.salt = salt
        self.fill()

    def fill(self):
        shape = self.layout.shape
        assert len(shape) == 2
        for x in range(shape[1]):
            for y in range(shape[0]):
                number = x*x + 3*x + 2*x*y + y + y*y
                number += self.salt
                n_bits = self.n_bits(number)
                if self.is_odd(n_bits):
                    self.layout[y, x] = 1

    @staticmethod
    def is_odd(n: int):
        return n % 2 == 1

    @staticmethod
    def n_bits(n: int):
        bin_str = '{0:b}'.format(n)
        return sum([int(c) for c in bin_str])

    def __str__(self):
        lst = [''.join([str(e) for e in line]) for line in self.layout.tolist()]
        string = '\n'.join(lst)
        string = string.replace('0', '.')
        string = string.replace('1', '#')
        string = string.replace('2', 'O')
        return string

    def steps_to(self, coord: Tuple[int, int]):
        old_layout = self.layout.copy()
        path = np.zeros_like(self.layout)
        mask = np.logical_not(self.layout)
        path[1, 1] = 1
        steps = 0
        while path[coord] == 0:
            path = binary_dilation(path, mask=mask)
            steps += 1
            self.layout = old_layout.copy()
            self.layout[path] = 2
        self.layout = old_layout
        return steps


def main():
    office = Office((50, 50), 1364)
    print(str(office))
    print(office.steps_to((39, 31)))


if __name__ == '__main__':
    main()