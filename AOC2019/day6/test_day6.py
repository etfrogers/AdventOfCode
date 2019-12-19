from AOC2019.day6.day6 import build_graph, count_orbits, get_transfers

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

test_input2 = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN'''


def test_1():
    graph = build_graph(test_input)
    total_orbits = count_orbits(graph)
    assert total_orbits == 42


def test_2():
    graph = build_graph(test_input2)
    transfers = get_transfers(graph)
    assert transfers == 4


def test_part1():
    with open('input.txt') as f:
        instructions = f.read()
    graph = build_graph(instructions)
    total_orbits = count_orbits(graph)
    assert total_orbits == 194721


def test_part2():
    with open('input.txt') as f:
        instructions = f.read()
    graph = build_graph(instructions)
    transfers = get_transfers(graph)
    assert transfers == 316
