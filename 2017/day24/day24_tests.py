import day24


def test_1():
    with open('test_input.txt', 'r') as file:
        components = file.readlines()
    components = [day24.Component(line) for line in components]
    bridges, strengths = day24.make_bridges(components)
    assert len(bridges) == 11
    assert max(strengths) == 31


def test_part1():
    with open('input.txt', 'r') as file:
        components = file.readlines()
    components = [day24.Component(line) for line in components]
    _, strengths = day24.make_bridges(components)
    assert max(strengths) == 1940


def test_2():
    with open('test_input.txt', 'r') as file:
        components = file.readlines()
    components = [day24.Component(line) for line in components]
    bridges, _ = day24.make_bridges(components)
    strength = day24.max_strength_long_bridge(bridges)
    assert strength == 19


def test_part2():
    with open('input.txt', 'r') as file:
        components = file.readlines()
    components = [day24.Component(line) for line in components]
    bridges, _ = day24.make_bridges(components)
    strength = day24.max_strength_long_bridge(bridges)
    assert strength == 1928
