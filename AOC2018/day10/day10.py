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
        self._initial_positions = np.vstack((p.position for p in self.points))
        self._velocities = np.vstack((p.velocity for p in self.points))

    def render_at(self, time, rng=None):
        xs = [p.position[0] for p in self.points]
        ys = [p.position[1] for p in self.points]

        pos = self.get_pos(time)
        if rng is None:
            x = list(range(min(xs), max(xs)+1))
            y = list(range(min(ys), max(ys)+1))
        else:
            x = range(np.min(pos[:, 0]), np.max(pos[:, 0])+1)
            y = range(np.min(pos[:, 1]), np.max(pos[:, 1])+1)

        sky = np.zeros((len(x), len(y)))
        any_point = False
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

    def get_pos(self, time):
        return self._initial_positions + self._velocities * time

    def find_message(self):
        min_var = 1000000000
        var = min_var
        min_time = 0

        time = 0
        while var < min_var*1.1:
            pos = self.get_pos(time)
            var = np.max(pos[:, 1]) - np.min(pos[:, 1])
            if var < min_var:
                min_time = time
                min_var = var
            time += 1
            if time == 10000000:
                return False
        return min_time


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

    msg_time = sky.find_message()
    print(msg_time)

    msg = sky.render_at(msg_time, (200, 200))
    print(msg)
