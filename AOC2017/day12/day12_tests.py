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


def test_2():
    with open('test_input.txt', 'r') as file:
        connections = file.readlines()
    connections = [line.strip() for line in connections]
    assert day12.count_groups(connections) == 2


def test_part2():
    with open('input.txt', 'r') as file:
        connections = file.readlines()
    connections = [line.strip() for line in connections]
    assert day12.count_groups(connections) == 202
