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


def test_balance_tower1():
    with open('test_input.txt', 'r') as file:
        data = file.readlines()
    data = [line.strip() for line in data]
    root_node = day7.create_tree(data)
    new_weight = day7.balance_tower(root_node)
    assert new_weight == 60


def test_part2():
    with open('input.txt', 'r') as file:
        data = file.readlines()
    data = [line.strip() for line in data]
    root_node = day7.create_tree(data)
    new_weight = day7.balance_tower(root_node)
    assert new_weight == 1526