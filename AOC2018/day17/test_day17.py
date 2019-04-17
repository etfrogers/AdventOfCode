from AOC2018.day17.day17 import Ground

test_input = '''x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504'''


def test_parsing():
    input_list = test_input.split('\n')
    ground = Ground(input_list)
    render = ground.render()
    assert render == blank_test_ground


def test_water_flow():
    input_list = test_input.split('\n')
    ground = Ground(input_list)
    ground.flow_water()
    render = ground.render()
    print(render)
    assert render == wet_test_ground


def test_water_amount():
    input_list = test_input.split('\n')
    ground = Ground(input_list)
    ground.flow_water()
    assert ground.amount_of_water == 57


blank_test_ground = '''......+.......
............#.
.#..#.......#.
.#..#..#......
.#..#..#......
.#.....#......
.#.....#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...'''

wet_test_ground = '''......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
...|||||||||..
...|#~~~~~#|..
...|#~~~~~#|..
...|#~~~~~#|..
...|#######|..'''