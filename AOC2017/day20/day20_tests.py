import day20


def test_close():
    with open('test_input.txt', 'r') as file:
        specs = file.readlines()
    specs = [spec.strip() for spec in specs]
    particles = [day20.Particle(*day20.Particle.parse_spec(spec)) for spec in specs]
    target = day20.get_closest_to_zero_long_term(particles)
    assert target == 0


def test_part1():
    with open('input.txt', 'r') as file:
        specs = file.readlines()
    specs = [spec.strip() for spec in specs]
    particles = [day20.Particle(*day20.Particle.parse_spec(spec)) for spec in specs]
    target = day20.get_closest_to_zero_long_term(particles)
    assert target == 170


def test_collisions():
    with open('test_input2.txt', 'r') as file:
        specs = file.readlines()
    specs = [spec.strip() for spec in specs]
    particles = [day20.Particle(*day20.Particle.parse_spec(spec)) for spec in specs]
    particles = day20.iterate(particles)
    assert len(particles) == 1


def test_part2():
    with open('input.txt', 'r') as file:
        specs = file.readlines()
    specs = [spec.strip() for spec in specs]
    particles = [day20.Particle(*day20.Particle.parse_spec(spec)) for spec in specs]
    particles = day20.iterate(particles)
    assert len(particles) == 571
