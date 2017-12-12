import day8


def test_build_memory1():
    with open('test_input.txt', 'r') as file:
        data = file.readlines()
    data = [line.strip() for line in data]
    print(data)
    max_val, _ = day8.build_memory(data)
    assert max_val == 1


def test_part1():
    with open('input.txt', 'r') as file:
        data = file.readlines()
    data = [line.strip() for line in data]
    max_val, _ = day8.build_memory(data)
    assert max_val == 4416


def test_build_memory2():
    with open('test_input.txt', 'r') as file:
        data = file.readlines()
    data = [line.strip() for line in data]
    print(data)
    _, all_time_max = day8.build_memory(data)
    assert all_time_max == 10
