package main

import (
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase = `O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....`

var testLines []string = strings.Split(testCase, "\n")

var tiltedLayout []string = make([]string, 4)

func init() {
	tiltedLayout[NORTH] = `OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....`
	tiltedLayout[SOUTH] = `.....#....
....#....#
...O.##...
...#......
O.O....O#O
O.#..O.#.#
O....#....
OO....OO..
#OO..###..
#OO.O#...O`
	tiltedLayout[WEST] = `O....#....
OOO.#....#
.....##...
OO.#OO....
OO......#.
O.#O...#.#
O....#OO..
O.........
#....###..
#OO..#....`
	tiltedLayout[EAST] = `....O#....
.OOO#....#
.....##...
.OO#....OO
......OO#.
.O#...O#.#
....O#..OO
.........O
#....###..
#..OO#....`
}

func TestBuild(t *testing.T) {
	rocks := NewRocks(testLines)
	assert.Equal(t, testCase, rocks.String())
}

func TestTilt(t *testing.T) {
	rocks := NewRocks(testLines)
	rocks.Tilt(NORTH)
	assert.Equal(t, tiltedLayout[NORTH], rocks.String())

	rocks = NewRocks(testLines)
	rocks.Tilt(SOUTH)
	assert.Equal(t, tiltedLayout[SOUTH], rocks.String())

	rocks = NewRocks(testLines)
	rocks.Tilt(WEST)
	assert.Equal(t, tiltedLayout[WEST], rocks.String())

	rocks = NewRocks(testLines)
	rocks.Tilt(EAST)
	assert.Equal(t, tiltedLayout[EAST], rocks.String())
}

func TestLoading(t *testing.T) {
	rocks := NewRocks(testLines)
	rocks.Tilt(NORTH)
	assert.Equal(t, 136, rocks.TotalLoading())
}

func TestPart1(t *testing.T) {
	lines := utils.ReadInput()
	rocks := NewRocks(lines)
	rocks.Tilt(NORTH)
	part1Answer := rocks.TotalLoading()
	assert.Equal(t, 109466, part1Answer)
}

var cycleOutputs []string = []string{
	`.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....`,
	`.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O`,
	`.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O`,
}

func TestCycle(t *testing.T) {
	rocks := NewRocks(testLines)
	for _, output := range cycleOutputs {
		rocks.Cycle()
		assert.Equal(t, output, rocks.String())
	}
}

func TestLoadingAfterN(t *testing.T) {
	rocks := NewRocks(testLines)
	expected := 64
	actual := rocks.GetLoadingAfterNCycles(1_000_000_000)
	assert.Equal(t, expected, actual)
}

func TestPart2(t *testing.T) {
	lines := utils.ReadInput()
	rocks := NewRocks(lines)
	part2Answer := rocks.GetLoadingAfterNCycles(1_000_000_000)
	assert.Equal(t, 94585, part2Answer)
}
