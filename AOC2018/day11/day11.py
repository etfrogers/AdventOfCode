import numpy as np
from scipy.signal import convolve2d

RACK_SIZE = (300, 300)
REGION = np.ones((3, 3))


class Rack:
    def __init__(self, serial):
        self.serial_number = serial
        x, y = np.meshgrid(np.arange(1, RACK_SIZE[1]+1), np.arange(1, RACK_SIZE[1]+1))
        rack_id = x + 10
        self.power_levels = rack_id * y
        self.power_levels += self.serial_number
        self.power_levels *= rack_id
        self.power_levels = hundreds_digit(self.power_levels)
        self.power_levels -= 5

    def __getitem__(self, item):
        return self.power_levels[item[1] - 1, item[0] - 1]

    def best_region(self):
        region_values = convolve2d(self.power_levels, REGION, mode='same')
        return tuple(reversed(np.unravel_index(np.argmax(region_values), region_values.shape)))


def hundreds_digit(val):
    frac = val / 100
    return np.round(np.floor(frac) - 10*np.floor(frac/10)).astype(int)


if __name__ == '__main__':
    rack = Rack(3999)
    print(rack.best_region())
