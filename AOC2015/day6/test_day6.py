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


def test_part_1():
    with open('input.txt') as f:
        instructions = f.readlines()
    lights = Lights()
    lights.process_instructions(instructions)
    assert lights.number_lit == 400410


def test_2():
    lights = Lights(part2=True)
    instructions = ['turn on 0,0 through 0,0']
    lights.process_instructions(instructions)
    assert lights.total_brightness == 1

    instructions = ['toggle 0,0 through 999,999']
    lights.process_instructions(instructions)
    assert lights.total_brightness == 2000000 + 1


def test_part_2():
    with open('input.txt') as f:
        instructions = f.readlines()
    lights = Lights(part2=True)
    lights.process_instructions(instructions)
    assert lights.total_brightness == 15343601
