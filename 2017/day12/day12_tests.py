import day12


def test_1():
    with open('test_input.txt', 'r') as file:
        connections = file.readlines()
    connections = [line.strip() for line in connections]
    assert day12.count_connections_to_node_zero(connections) == 6


def test_part1():
    with open('input.txt', 'r') as file:
        connections = file.readlines()
    connections = [line.strip() for line in connections]
    assert day12.count_connections_to_node_zero(connections) == 113
