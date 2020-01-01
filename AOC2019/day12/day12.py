import itertools
import re
import numpy as np

from utils import Point

FORMAT = '{:>2}'
COORD_TEMPLATE = '<x={}, y={}, z={}>'.format(*[FORMAT] * 3)
COORD_PATTERN = COORD_TEMPLATE.replace(FORMAT, r'([- 0-9]*)')
COORD_REGEX = re.compile(COORD_PATTERN)
MOON_REGEX = re.compile('pos=' + COORD_PATTERN + ', vel=' + COORD_PATTERN)


class Point3D(Point):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __str__(self):
        return COORD_TEMPLATE.format(*iter(self))


class Moon:
    def __init__(self, spec=None):
        if spec is not None:
            matches = COORD_REGEX.match(spec)
            coords = [int(v) for v in matches.groups()]
            self.pos = Point3D(*coords)
        else:
            self.pos = Point3D(0, 0, 0)
        self.vel = Point3D(0, 0, 0)

    def __str__(self):
        return 'pos=' + str(self.pos) + ', vel=' + str(self.vel)

    def __eq__(self, other):
        return self.pos == other.pos and self.vel == other.vel

    @staticmethod
    def build_from_test_data(string):
        matches = MOON_REGEX.match(string)
        moon = Moon()
        pos_coords = [int(v) for v in matches.groups()[:3]]
        vel_coords = [int(v) for v in matches.groups()[3:]]
        moon.pos = Point3D(*pos_coords)
        moon.vel = Point3D(*vel_coords)
        return moon

    def move(self):
        self.pos += self.vel

    def energy(self):
        return self.pos.norm(1) * self.vel.norm(1)

    def tuple(self, axis=None):
        if axis is None:
            return self.pos.tuple, self.vel.tuple
        else:
            return self.pos.tuple[axis], self.vel.tuple[axis]


class MoonSet:
    def __init__(self, specs=None):
        if specs is not None:
            self.moons = [Moon(spec) for spec in specs.split('\n')]
        else:
            self.moons = []

    def __str__(self):
        return '\n'.join([str(moon) for moon in self.moons])

    def __eq__(self, other):
        return all([s == o for s, o in zip(self.moons, other.moons)])

    @staticmethod
    def build_from_test_data(data):
        moons = MoonSet()
        moons.moons = [Moon.build_from_test_data(spec) for spec in data]
        return moons

    def run(self, n_steps):
        for _ in range(n_steps):
            self.apply_step()

    def apply_step(self):
        self.apply_gravity()
        self.move()

    def move(self):
        for moon in self.moons:
            moon.move()

    def find_first_repeat(self, lcm=True):
        if not lcm:
            i = 0
            visited = set()
            while self.tuple() not in visited:
                visited.add(self.tuple())
                i += 1
                self.apply_step()
            return i
        else:
            visited = [set(), set(), set()]
            i = 0
            found = [0] * 3
            while not all(found):
                for axis in range(3):
                    tup = self.tuple(axis)
                    if tup in visited[axis] and not found[axis]:
                        found[axis] = i
                    if found[axis]:
                        continue
                    visited[axis].add(tup)
                i += 1
                self.apply_step()
            return np.lcm.reduce(found)

    def apply_gravity(self):
        for moon1, moon2 in itertools.combinations(self.moons, 2):
            if moon1.pos.x < moon2.pos.x:
                moon1.vel.x += 1
                moon2.vel.x -= 1
            elif moon1.pos.x > moon2.pos.x:
                moon1.vel.x -= 1
                moon2.vel.x += 1
            if moon1.pos.y < moon2.pos.y:
                moon1.vel.y += 1
                moon2.vel.y -= 1
            elif moon1.pos.y > moon2.pos.y:
                moon1.vel.y -= 1
                moon2.vel.y += 1
            if moon1.pos.z < moon2.pos.z:
                moon1.vel.z += 1
                moon2.vel.z -= 1
            elif moon1.pos.z > moon2.pos.z:
                moon1.vel.z -= 1
                moon2.vel.z += 1

    def total_energy(self):
        return sum([moon.energy() for moon in self.moons])

    def tuple(self, axis=None):
        return tuple([moon.tuple(axis) for moon in self.moons])


def main():
    with open('input.txt') as file:
        specs = file.read()
    n = 1000
    moons = MoonSet(specs)
    moons.run(n)
    print(f'Total energy after {n} steps is {moons.total_energy()}')

    moons = MoonSet(specs)
    repeat = moons.find_first_repeat()
    print(f'First repeat is after {repeat} steps')


if __name__ == '__main__':
    main()
