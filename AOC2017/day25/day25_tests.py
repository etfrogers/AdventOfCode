import day25


def test_1():
    with open('test_input.txt', 'r') as file:
        blueprints = file.read()
    tm = day25.TuringMachine(blueprints)
    tm.run()
    assert tm.get_checksum() == 3


def test_part1():
    with open('input.txt', 'r') as file:
        blueprints = file.read()
    tm = day25.TuringMachine(blueprints)
    tm.run()
    assert tm.get_checksum() == 2832
