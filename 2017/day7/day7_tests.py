import day7


def test_create_tree1():
    with open('test_input.txt', 'r') as file:
        data = file.readlines()
    data = [line.strip() for line in data]
    assert day7.create_tree(data).name == 'tknk'


def test_part1():
    with open('input.txt', 'r') as file:
        data = file.readlines()
    data = [line.strip() for line in data]
    assert day7.create_tree(data).name == 'gynfwly'

