import pytest

from AOC2019.day11.day11 import PaintBot
from intcode import IntCodeComputer

test_data = [(1, 0), (0, 0), (1, 0), (1, 0), (0, 1), (1, 0), (1, 0)]
cases = [(0, 0, '''.....
.....
..^..
.....
.....'''),
         (1, 0, '''.....
.....
.<#..
.....
.....'''),
         (2, 0, '''.....
.....
..#..
.v...
.....'''),
         (4, 1, '''.....
.....
..^..
.##..
.....'''),
         (7, 0, '''.....
..<#.
...#.
.##..
.....''')]


@pytest.mark.parametrize('n, _, expected_output', cases)
def test_1(n, _, expected_output):
    # comp = IntCodeComputer('input.txt', [])
    bot = PaintBot(fake_data=test_data[:n])
    bot.build_panels()
    string = bot.render(override_size=5)
    assert string == expected_output
    print(bot.fake_input)
    if n > 0:
        assert len(bot.fake_input) == n
    if n > 4:
        assert bot.fake_input[4] == 1


def test_2():
    bot = PaintBot(fake_data=test_data)
    bot.build_panels()
    assert len(bot.panels) == 6


def test_part1():
    comp = IntCodeComputer('input.txt', [])
    bot = PaintBot(comp)
    bot.build_panels(debug=False)
    # print(bot.render())
    assert len(bot.panels) == 1686


def test_part2():
    comp = IntCodeComputer('input.txt', [])
    bot = PaintBot(comp, initial_color=1)
    bot.build_panels()
    # Identifier is GARPKZUL
    assert bot.render() == '''..##...##..###..###..#..#.####.#..#.#......
.#..#.#..#.#..#.#..#.#.#.....#.#..#.#......
.#....#..#.#..#.#..#.##.....#..#..#.#......
.#.##.####.###..###..#.#...#...#..#.#......
.#..#.#..#.#.#..#....#.#..#....#..#.#....>.
..###.#..#.#..#.#....#..#.####..##..####...'''
