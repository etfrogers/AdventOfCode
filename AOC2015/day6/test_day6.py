from AOC2015.day6.day6 import Lights


def test_1():
    lights = Lights()
    instructions = ['turn on 0,0 through 999,999']
    lights.process_instructions(instructions)
    assert lights.number_lit == 1000000

    instructions = ['toggle 0,0 through 999,0']
    lights.process_instructions(instructions)
    assert lights.number_lit == 1000000 - 1000

    instructions = ['turn off 499,499 through 500,500']
    lights.process_instructions(instructions)
    assert lights.number_lit == 1000000 - 1000 - 4
