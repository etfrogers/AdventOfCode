import day8


def test_1():
    screen = day8.Screen(7, 3)
    commands = ['rect 3x2']
    result = '''###....
###....
.......'''
    screen.run(commands)
    assert str(screen) == result


def test_2():
    screen = day8.Screen(7, 3)
    commands = ['rect 3x2', 'rotate column x=1 by 1']
    result = '''#.#....
###....
.#.....'''
    screen.run(commands)
    assert str(screen) == result


def test_3():
    screen = day8.Screen(7, 3)
    commands = ['rect 3x2', 'rotate column x=1 by 1', 'rotate row y=0 by 4']
    result = '''....#.#
###....
.#.....'''
    screen.run(commands)
    assert str(screen) == result


def test_4():
    screen = day8.Screen(7, 3)
    commands = ['rect 3x2', 'rotate column x=1 by 1', 'rotate row y=0 by 4', 'rotate column x=1 by 1']
    result = '''.#..#.#
#.#....
.#.....'''
    screen.run(commands)
    assert str(screen) == result
