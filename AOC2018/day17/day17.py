import re
from typing import List, Tuple

import numpy as np

SAND = 0
CLAY = 1
FLOW = 2
WATER = 3
SPRING = 4

SYMBOLS = {SAND: '.',
           CLAY: '#',
           FLOW: '|',
           WATER: '~',
           SPRING: '+',
           }


class Spec:
    line_pattern = re.compile(r'([xy])=([0-9]+), ([xy])=([0-9]+)\.\.([0-9]+)')

    def __init__(self, line: str):
        matches = self.line_pattern.match(line).groups()
        if matches[0] == 'x':
            self.x_start = int(matches[1])
            self.x_stop = self.x_start
            assert matches[2] == 'y'
            self.y_start = int(matches[3])
            self.y_stop = int(matches[4])
        else:
            self.y_start = int(matches[1])
            self.y_stop = self.y_start
            assert matches[2] == 'x'
            self.x_start = int(matches[3])
            self.x_stop = int(matches[4])
        assert self.x_start <= self.x_stop
        assert self.y_start <= self.y_stop


class Ground:
    SPRING_X = 500
    SPRING_Y = 0

    def __init__(self, spec: List[str]):
        specs = [Spec(line) for line in spec]
        self.map_ = None
        self.x = self.y = None
        self.build_map(specs)

    def build_map(self, specs: List[Spec]):
        min_x = min([s.x_start for s in specs])
        max_x = max([s.x_stop for s in specs])
        min_y = min([s.y_start for s in specs])
        max_y = max([s.y_stop for s in specs])
        assert min_x < self.SPRING_X
        assert max_x > self.SPRING_X

        self.x = np.arange(min_x-1, max_x+1+1)
        self.y = np.arange(min_y, max_y+1)
        self.map_ = np.full((self.y.size, self.x.size), SAND)
        for spec in specs:
            self[spec.y_start:spec.y_stop+1, spec.x_start:spec.x_stop+1] = CLAY

    def transform_slices(self, key):
        assert len(key) == 2
        offsets = (self.y_offset, self.x_offset)
        output = []
        for i, index in enumerate(key):
            if isinstance(index, int) or isinstance(index, np.int64):
                index -= offsets[i]
            elif isinstance(index, slice):
                start, stop, step = index.start, index.stop, index.step  # index is a slice
                start -= offsets[i]
                stop -= offsets[i]
                index = slice(start, stop, step)
            else:
                raise TypeError("index must be int, slice or array")
            output.append(index)
        return tuple(output)

    @property
    def shape(self):
        return self.map_.shape

    @property
    def x_offset(self):
        return int(self.x[0])

    @property
    def y_offset(self):
        return int(self.y[0])

    def __getitem__(self, item):
        return self.map_[self.transform_slices(item)]

    def __setitem__(self, key, value):
        self.map_[self.transform_slices(key)] = value

    def render(self) -> str:
        render = np.full_like(self.map_, '', dtype=str)
        pad_size = self.y_offset
        for k, v in SYMBOLS.items():
            render[self.map_ == k] = v
        render = np.pad(render, ((pad_size, 0), (0, 0)), 'constant', constant_values=SYMBOLS[SAND])
        render[self.transform_slices((self.SPRING_Y+pad_size, self.SPRING_X))] = SYMBOLS[SPRING]
        lines = [''.join(line) for line in render.tolist()]
        return '\n'.join(lines)

    def flow_water(self):
        streams = [Stream(self, (self.y_offset, self.SPRING_X))]
        while streams:
            stream = streams.pop()
            new_streams = stream.flow()
            if new_streams:
                streams.extend(new_streams)

    @property
    def amount_of_water(self):
        return np.count_nonzero(np.logical_or(self.map_ == FLOW, self.map_ == WATER))


class Stream:
    DOWN = np.array([1, 0])
    UP = np.array([-1, 0])
    LEFT = np.array([0, -1])
    RIGHT = np.array([0, 1])

    def __init__(self, ground: Ground, coords: Tuple[int, int]):
        self.ground = ground
        self.coords = np.array(coords)

    def flow(self):
        new_streams = []
        # set start point to flow
        self.ground[self.coords] = FLOW

        # go down until you hit clay, water or the bottom
        while (self.coords + self.DOWN)[0] <= np.max(self.ground.y) and self.ground[self.coords + self.DOWN] == SAND:
            self.coords += self.DOWN
            self.ground[self.coords] = FLOW

        # if at the bottom,or have hit flowing water, stop and and do not create streams
        if (self.coords + self.DOWN)[0] > np.max(self.ground.y) or \
                self.ground[self.coords + self.DOWN] == FLOW:
            return []

        flow_found = False
        # fill up a basin
        while True:
            # record where we stopped so we can go back there
            stopping_point = self.coords.copy()
            # cache collects the current layer, which will be set to WATER (if static) or FLOW if not.
            cache = [tuple(self.coords)]
            cache_type = WATER

            # go left/right until you hit clay or an open square to drop over
            for direction in self.LEFT, self.RIGHT:
                while self.ground[self.coords + direction] != CLAY:
                    self.coords += direction
                    cache.append(tuple(self.coords))
                    # if we are on an open square, set layer type to water and create a new stream point.
                    if self.ground[self.coords + self.DOWN] == SAND:
                        cache.append(tuple(self.coords))
                        cache_type = FLOW
                        new_streams.append(Stream(self.ground, self.coords.copy()))
                        break
                    elif self.ground[self.coords + self.DOWN] == FLOW:
                        # need to exit if we have flow below (but without creating a stream)
                        # without this section, it progresses beyond the flow, creating two parallel flows
                        flow_found = True
                        cache.append(tuple(self.coords))
                        cache_type = FLOW
                        break
                self.coords = stopping_point.copy()
            # set points in current layer to correct type
            for point in cache:
                self.ground[point] = cache_type
            # if we made any new streams we have finished this stream, so break out
            if new_streams or flow_found:
                break
            self.coords = stopping_point + self.UP
        return new_streams


def main():
    with open('input.txt') as file:
        specs = file.readlines()
    ground = Ground(specs)
    # print(ground.render())
    # print()
    ground.flow_water()
    print(ground.render())
    print(f'Part 1: {ground.amount_of_water}')


if __name__ == '__main__':
    main()
