from AOC2018.day12 import day12


test_input = '''initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #'''

test_initial_state, test_mapping_string = test_input.split('\n\n')

test_plants = day12.Plants(test_initial_state, test_mapping_string)
test_plants.fill_unfilled_mapping()

test_results = '''...#..#.#..##......###...###...........
...#...#....#.....#..#..#..#...........
...##..##...##....#..#..#..##..........
..#.#...#..#.#....#..#..#...#..........
...#.#..#...#.#...#..#..##..##.........
....#...##...#.#..#..#...#...#.........
....##.#.#....#...#..##..##..##........
...#..###.#...##..#...#...#...#........
...#....##.#.#.#..##..##..##..##.......
...##..#..#####....#...#...#...#.......
..#.#..#...#.##....##..##..##..##......
...#...##...#.#...#.#...#...#...#......
...##.#.#....#.#...#.#..##..##..##.....
..#..###.#....#.#...#....#...#...#.....
..#....##.#....#.#..##...##..##..##....
..##..#..#.#....#....#..#.#...#...#....
.#.#..#...#.#...##...#...#.#..##..##...
..#...##...#.#.#.#...##...#....#...#...
..##.#.#....#####.#.#.#...##...##..##..
.#..###.#..#.#.#######.#.#.#..#.#...#..
.#....##....#####...#######....#.#..##.'''


def generation_matches(a, b):
    assert a == b


def test_1():
    test_list = test_results.split('\n')
    for i, result in enumerate(test_list):
        yield generation_matches, test_plants.get_generation(i)[-3:36], result


def test_2():
    assert test_plants.checksum(20) == 325


def test_part1():
    with open('input.txt') as f:
        input_ = f.read()
    initial_state, mapping_string = input_.split('\n\n')

    plants = day12.Plants(initial_state, mapping_string)

    assert plants.checksum(20) == 4818


def test_part2():
    with open('input.txt') as f:
        input_ = f.read()
    initial_state, mapping_string = input_.split('\n\n')

    plants = day12.Plants(initial_state, mapping_string)

    assert plants.large_checksum(50000000000) == 5100000001377
