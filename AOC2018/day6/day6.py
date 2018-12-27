import string

import numpy as np


class Space:
    def __init__(self, input_, label_strs=None):
        if type(input_) is str:
            input_ = input_.split('\n')
        pts = [line.split(', ') for line in input_]
        self.points = np.array(pts, dtype=int)
        self.labels = np.arange(1, len(self.points)+1)[np.newaxis, np.newaxis, :]
        x_ = np.arange(np.min(self.points[:, 0]) - 1, np.max(self.points[:, 0] + 2))
        y_ = np.arange(np.min(self.points[:, 1]) - 1, np.max(self.points[:, 1] + 2))
        self.x, self.y = np.meshgrid(x_, y_)
        self.map = np.zeros_like(self.x)
        self.totals = np.zeros_like(self.x)
        self.label_strs = label_strs

    def render(self):
        map = self.map.astype(dtype=str)
        map[np.where(self.map == 0)] = '.'
        for pt, label in zip(self.points, self.labels[0, 0, :]):
            map[np.where(self.map == label)] = self.num_to_label(label, uppercase=False)
            map[np.logical_and(self.x == pt[0], self.y == pt[1])] = self.num_to_label(label)
        map = map.tolist()
        map = '\n'.join([''.join(line) for line in map])
        return map

    def build_regions(self):
        pt_x = self.points[:, 0]
        pt_y = self.points[:, 1]
        dists = np.abs(self.x[:, :, np.newaxis] - pt_x[np.newaxis, np.newaxis, :]) + \
                np.abs(self.y[:, :, np.newaxis] - pt_y[np.newaxis, np.newaxis, :])
        self.totals = np.sum(dists, 2)

        min_ind = np.argmin(dists, 2)
        min_val = np.min(dists, 2)
        tied = np.sum(dists == min_val[:, :, np.newaxis], 2) > 1
        self.map = self.labels[0, 0, min_ind]
        self.map[tied] = 0

    def sizes(self):
        finite_map = self.map.copy()
        edge_labels = set(np.concatenate((finite_map[ 0, :].flatten(),
                                          finite_map[-1, :].flatten(),
                                          finite_map[:,  0].flatten(),
                                          finite_map[:, -1].flatten())).tolist())

        return {self.num_to_label(label): np.sum(self.map == label) if label not in edge_labels else -1
                for label in self.labels.flatten().tolist()}

    def num_to_label(self, num, uppercase=True):
        if self.label_strs is not None:
            val = self.label_strs[num-1]
            val = val.upper() if uppercase else val.lower()
        else:
            val = num
        return val

    def safest_place(self):
        sizes = self.sizes()
        return max(sizes.keys(), key=lambda key: sizes[key])

    def safest_size(self):
        sizes = self.sizes()
        return max(sizes.values())

    def safe_region_size(self, dist):
        safe_space = self.totals < dist
        return np.sum(safe_space)


def main():
    with open('input.txt') as f:
        input_ = f.read()
    space = Space(input_)
    space.build_regions()
    print('Part 1: ', space.safest_size())
    print('Part 2: ', space.safe_region_size(10000))


if __name__ == '__main__':
    main()
