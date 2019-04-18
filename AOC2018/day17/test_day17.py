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
    assert render == wet_test_ground


def test_water_amount():
    input_list = test_input.split('\n')
    ground = Ground(input_list)
    ground.flow_water()
    assert ground.amount_of_water == 57


def test_loops():
    input_list = loop_input.split('\n')
    ground = Ground(input_list)
    ground.flow_water()
    render = ground.render()
    assert render == loop_result


def test_anti_loop():
    input_list = anti_loop_input.split('\n')
    ground = Ground(input_list)
    ground.flow_water()
    render = ground.render()
    assert render == anti_loop_result


anti_loop_input = '''y=6, x=499..501
x=499, y=3..6
x=501, y=5..6
x=505, y=1..2
x=505, y=3..9
x=495, y=3..9
y=9, x=495..505'''


loop_input = '''y=4, x=499..501
x=499, y=3..4
x=501, y=3..4
x=505, y=1..2
x=505, y=7..9
x=495, y=7..9
y=9, x=495..505'''


loop_result = '''......+......
......|....#.
....|||||..#.
....|#~#|....
....|###|....
....|...|....
|||||||||||||
|#~~~~~~~~~#|
|#~~~~~~~~~#|
|###########|'''

anti_loop_result = '''......+......
......|....#.
|||||||||||#.
|#~~~#~~~~~#.
|#~~~#~~~~~#.
|#~~~#~#~~~#.
|#~~~###~~~#.
|#~~~~~~~~~#.
|#~~~~~~~~~#.
|###########.'''

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