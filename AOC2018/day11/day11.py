import numpy as np
from scipy.signal import convolve

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

    def best_region(self, size=None):
        if size is None:
            region = REGION
            size = 3
        else:
            region = np.ones((size, size))
        return find_max_region(self.power_levels, region)

    def best_region_scan_size(self):
        sizes = range(1, RACK_SIZE[0] + 1)
        best_coords, best_vals = zip(*[self.best_region(size) for size in sizes])
        max_index = np.argmax(best_vals)
        return best_coords[max_index] + (sizes[max_index], )


def find_max_region(array, region):
    size = region.shape[0]
    assert all([s == size for s in region.shape])
    region_values = convolve(array, region, mode='same')
    # round because convolve can use fft which gives floats. In this case we know all vals are integer
    region_values = np.round(region_values).astype(int)
    best_val = np.max(region_values)
    best_coords = tuple(reversed(np.unravel_index(np.argmax(region_values), region_values.shape)))
    # convert for top left corner
    best_coords = tuple(c + 1 - int(np.floor(size / 2)) for c in best_coords)
    return best_coords, best_val


def hundreds_digit(val):
    frac = val / 100
    return np.round(np.floor(frac) - 10*np.floor(frac/10)).astype(int)


if __name__ == '__main__':
    rack = Rack(3999)
    print(rack.best_region())

    print(rack.best_region_scan_size())
