from AOC2016.day23.day23 import AssemBunnyInterpreter23, python_translation


def test_1():
    test_input = '''cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a'''
    interp = AssemBunnyInterpreter23(test_input.split('\n'))
    interp.execute()
    assert interp.registers['a'] == 3


def test_part_1():
    with open('input.txt') as file:
        prog = file.readlines()
    interp = AssemBunnyInterpreter23(prog)
    interp.registers['a'] = 7
    interp.execute(show_status=False)
    assert interp.registers['a'] == 12775


def test_part_1_python():
    a = python_translation(7)
    assert a == 12775
