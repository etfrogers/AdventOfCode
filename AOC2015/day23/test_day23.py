from AOC2015.day23.day23 import Interpreter2015


def test_1():
    test_input = '''inc a
jio a, +2
tpl a
inc a'''
    interp = Interpreter2015(test_input.split('\n'))
    interp.execute(show_status=True)
    assert interp.registers['a'] == 2
