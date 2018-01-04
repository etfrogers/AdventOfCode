import re
from collections import Counter
vec_re = re.compile('[pva]=<([0-9, -]*)>')


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def norm(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __str__(self):
        return '<%i,%i,%i>' % (self.x, self.y, self.z)


class Particle:
    def __init__(self, p, v, a):
        self.p = p
        self.v = v
        self.a = a

    @staticmethod
    def parse_spec(spec):
        parts = spec.split(', ')
        assert all([p.startswith(label) for p, label in zip(parts, ['p=', 'v=', 'a='])])
        # print(parts)
        return (string_to_vec(p) for p in parts)

    def tick(self):
        self.v += self.a
        self.p += self.v

    def __str__(self):
        return str(self.p)


def string_to_vec(string):
    match = re.match(vec_re, string)
    vec_string = match.group(1)
    vec_ints = (int(v) for v in vec_string.split(','))
    return Vector(*vec_ints)


def get_closest_to_zero_long_term(particles):
    sorted_particles = sorted(particles, key=lambda p: p.a.norm())
    low_velocity_particles = [p for p in particles if p.a.norm() == sorted_particles[0].a.norm()]
    sorted_low_v_particles = sorted(low_velocity_particles, key=lambda p: p.v.norm())
    return particles.index(sorted_low_v_particles[0])


def tick(particles):
    for p in particles:
        p.tick()


def iterate(particles):
    for i in range(1000):
        tick(particles)
        # remove particles with duplicate positions
        positions = [str(p) for p in particles]
        pos_counts = Counter(positions)
        particles = [part for pos, part in zip(positions, particles) if pos_counts[pos] == 1]
    return particles


def main():
    with open('input.txt', 'r') as file:
        specs = file.readlines()
    specs = [spec.strip() for spec in specs]

    particles = [Particle(*Particle.parse_spec(spec)) for spec in specs]
    print([str(p) for p in particles])
    particles = iterate(particles)
    print([str(p) for p in particles])
    print(len(particles))


if __name__ == '__main__':
    main()
