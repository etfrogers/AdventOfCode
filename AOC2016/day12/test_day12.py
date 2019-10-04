from AOC2016.day12.day12 import AssemBunnyInterpreter


def test1():
    program = '''cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a'''
    interp = AssemBunnyInterpreter(program.split('\n'))
    interp.execute()
    assert interp.registers['a'] == 42


def test_part1():
    with open('input.txt') as file:
        prog = file.readlines()
    interp = AssemBunnyInterpreter(prog)
    interp.execute()
    assert interp.registers['a'] == 318003


def test_part2():
    with open('input.txt') as file:
        prog = file.readlines()
    interp = AssemBunnyInterpreter(prog)
    interp.registers['c'] = 1
    interp.execute()
    assert interp.registers['a'] == 9227657
