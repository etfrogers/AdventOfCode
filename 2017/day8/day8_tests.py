import day8


def test_build_memory1():
    with open('test_input.txt', 'r') as file:
        data = file.readlines()
    data = [line.strip() for line in data]
    print(data)
    assert day8.build_memory(data) == 1


def test_part1():
    with open('input.txt', 'r') as file:
        data = file.readlines()
    data = [line.strip() for line in data]
    assert day8.build_memory(data) == 4416
