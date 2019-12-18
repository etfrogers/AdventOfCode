from AOC2019.day6.day6 import build_graph, count_orbits

test_input = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L'''


def test_1():
    graph = build_graph(test_input)
    total_orbits = count_orbits(graph)
    assert total_orbits == 42


def test_part1():
    with open('input.txt') as f:
        instructions = f.read()
    graph = build_graph(instructions)
    total_orbits = count_orbits(graph)
    assert total_orbits == 194721
