import re
vec_re = re.compile('[pva]=<([0-9, -]*)>')


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def norm(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


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


def string_to_vec(string):
    match = re.match(vec_re, string)
    vec_string = match.group(1)
    vec_ints = (int(v) for v in vec_string.split(','))
    return Vector(*vec_ints)


def get_closest_to_zero_long_term(particles):
    sorted_particles = sorted(particles, key=lambda p: p.a.norm())
    # for i, p in enumerate(sorted_particles):
    #     print(i, p.a.norm())
    low_velocity_particles = [p for p in particles if p.a.norm() == sorted_particles[0].a.norm()]
    # print(low_velocity_particles)
    sorted_low_v_particles = sorted(low_velocity_particles, key=lambda p: p.v.norm())
    return particles.index(sorted_low_v_particles[0])


def main():
    with open('input.txt', 'r') as file:
        specs = file.readlines()
    specs = [spec.strip() for spec in specs]

    particles = [Particle(*Particle.parse_spec(spec)) for spec in specs]
    print(particles)
    target = get_closest_to_zero_long_term(particles)
    print(target)


if __name__ == '__main__':
    main()
