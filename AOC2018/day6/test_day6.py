from AOC2018.day6 import day6


test_input = '''1, 1
1, 6
8, 3
3, 4
5, 5
8, 9'''


test_output_prebuild = '''..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
..........'''


test_ouput = '''aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
bbb.ffffff'''


test_labels = 'ABCDEF'


def test_prebuild():
    space = day6.Space(test_input, test_labels)
    assert space.render() == test_output_prebuild


def test_render():
    space = day6.Space(test_input, test_labels)
    space.build_regions()
    calc_output = space.render()
    assert calc_output == test_ouput


def test_1():
    test_sizes = {'A': -1, 'B': -1, 'C': -1, 'D': 9, 'E': 17, 'F': -1}
    space = day6.Space(test_input, test_labels)
    space.build_regions()
    sizes = space.sizes()
    assert all([sizes[key] == test_sizes[key] for key in test_sizes.keys()])


def test_2():
    space = day6.Space(test_input, test_labels)
    space.build_regions()
    assert space.safest_place() == 'E'


def test_3():
    space = day6.Space(test_input, test_labels)
    space.build_regions()
    assert space.safest_size() == 17


def test_part1():
    with open('input.txt') as f:
        input_ = f.read()
    space = day6.Space(input_)
    space.build_regions()
    assert space.safest_size() == 4771


def test_safe_region_size():
    space = day6.Space(test_input, test_labels)
    space.build_regions()
    assert space.safe_region_size(32) == 16


def test_part2():
    with open('input.txt') as f:
        input_ = f.read()
    space = day6.Space(input_)
    space.build_regions()
    assert space.safe_region_size(10000) == 39149
