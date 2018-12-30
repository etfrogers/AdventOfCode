from AOC2018.day18 import day18

test_states = '''Initial state:
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.

After 1 minute:
.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|.

After 2 minutes:
.......#..
......|#..
.|.|||....
..##|||..#
..###|||#|
...#|||||.
|||||||||.
||||||||||
||||||||||
.|||||||||

After 3 minutes:
.......#..
....|||#..
.|.||||...
..###|||.#
...##|||#|
.||##|||||
||||||||||
||||||||||
||||||||||
||||||||||

After 4 minutes:
.....|.#..
...||||#..
.|.#||||..
..###||||#
...###||#|
|||##|||||
||||||||||
||||||||||
||||||||||
||||||||||

After 5 minutes:
....|||#..
...||||#..
.|.##||||.
..####|||#
.|.###||#|
|||###||||
||||||||||
||||||||||
||||||||||
||||||||||

After 6 minutes:
...||||#..
...||||#..
.|.###|||.
..#.##|||#
|||#.##|#|
|||###||||
||||#|||||
||||||||||
||||||||||
||||||||||

After 7 minutes:
...||||#..
..||#|##..
.|.####||.
||#..##||#
||##.##|#|
|||####|||
|||###||||
||||||||||
||||||||||
||||||||||

After 8 minutes:
..||||##..
..|#####..
|||#####|.
||#...##|#
||##..###|
||##.###||
|||####|||
||||#|||||
||||||||||
||||||||||

After 9 minutes:
..||###...
.||#####..
||##...##.
||#....###
|##....##|
||##..###|
||######||
|||###||||
||||||||||
||||||||||

After 10 minutes:
.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||'''


states = test_states.split('\n\n')
states = ['\n'.join(state.split('\n')[1:]) for state in states]
# area = day18.Area(states[0])


def test_initial_render():
    area = day18.Area(states[0])
    assert area.render() == states[0]


def check_state(area, state):
    result = area.render()
    assert result == state


def test_evolution():
    area = day18.Area(states[0])
    for state in states[1:]:
        area.evolve()
        yield check_state, area, state


def check_centre_of_single_step(initial_state, expected_in_centre):
    area = day18.Area(initial_state)
    area.evolve()
    assert day18.LandType(area.layout[1, 1]) == expected_in_centre


def test_manual_states():
    states = [('...\n...\n.||', day18.LandType.OPEN),
              ('...\n...\n|||', day18.LandType.TREES),
              ('###\n#.|\n.||', day18.LandType.TREES),
              ('###\n#.#\n#||', day18.LandType.OPEN),

              ('|||\n|||\n|||', day18.LandType.TREES),
              ('...\n|||\n...', day18.LandType.TREES),
              ('###\n|||\n|||', day18.LandType.LUMBERYARD),
              ('...\n#|#\n...', day18.LandType.TREES),
              ('...\n#|#\n|#|', day18.LandType.LUMBERYARD),
              ('|||\n|||\n|||', day18.LandType.TREES),

              ('|||\n|#|\n|||', day18.LandType.OPEN),
              ('###\n###\n###', day18.LandType.OPEN),
              ('|||\n|#|\n|#|', day18.LandType.LUMBERYARD),
              ('...\n.#.\n...', day18.LandType.OPEN),
              ('...\n.#.\n.#|', day18.LandType.LUMBERYARD),
              ]
    for state in states:
        yield check_centre_of_single_step, state[0], state[1]


def test_resources():
    area = day18.Area(states[0])
    area.evolve(n=10)
    assert area.total_resources == 1147


def test_part1():
    with open('input.txt') as f:
        initial_state = f.read()
    area = day18.Area(initial_state)
    area.evolve(10)
    assert area.total_resources == 536370


def test_total_non_loop():
    with open('input.txt') as f:
        initial_state = f.read()
    area = day18.Area(initial_state)
    assert area.get_total_resources(10) == 536370


def test_part2():
    with open('input.txt') as f:
        initial_state = f.read()
    area = day18.Area(initial_state)
    n = 1000000000
    assert area.get_total_resources(n) == 190512
