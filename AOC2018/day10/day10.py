import re
from time import sleep

import numpy as np

LINE_PATTERN = re.compile(r'position=< *(-?[0-9]+), *(-?[0-9]+)> velocity=< *(-?[0-9]+), *(-?[0-9]+)>')


class Point:
    def __init__(self, line):
        matches = LINE_PATTERN.match(line)
        px, py, vx, vy = (int(v) for v in matches.groups())
        self.position = np.array([px, py])
        self.velocity = np.array([vx, vy])


class Sky:
    def __init__(self, instructions):
        self.points = [Point(line) for line in instructions]

    def render_at(self, time):
        xs = [p.position[0] for p in self.points]
        ys = [p.position[1] for p in self.points]

        x = list(range(min(xs), max(xs)+1))
        y = list(range(min(ys), max(ys)+1))
        x = range(-100, 100)
        y = range(-100, 100)

        sky = np.zeros((len(x), len(y)))
        any_point = False
        # initial_positions = np.vstack((p.position for p in self.points))
        for point in self.points:
            pos = point.position + point.velocity * time
            try:
                px = x.index(pos[0])
                py = y.index(pos[1])
                sky[px, py] = 1
                any_point = True
            except ValueError:
                pass
        return sky_array_to_string(sky) if any_point else None


def sky_array_to_string(array: np.ndarray):
    lines = array.transpose().tolist()
    lines = [''.join([str(int(v)) for v in line]) for line in lines]
    string = '\n'.join(lines)
    string = string.replace('0', '.')
    string = string.replace('1', '#')
    return string


if __name__ == '__main__':
    with open('input.txt') as f:
        input_ = f.readlines()
    input_ = [line.strip() for line in input_]
    sky = Sky(input_)
    for i in range(100000):
        string = sky.render_at(i)
        if string:
            print(string)
            sleep(1)
        elif i % 100 == 0:
            print(i)
