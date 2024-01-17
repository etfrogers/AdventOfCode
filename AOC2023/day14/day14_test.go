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

var tiltedLayout = `OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....`

func TestBuild(t *testing.T) {
	rocks := NewRocks(testLines)
	assert.Equal(t, testCase, rocks.String())
}

func TestTilt(t *testing.T) {
	rocks := NewRocks(testLines)
	rocks.Tilt(NORTH)
	assert.Equal(t, tiltedLayout, rocks.String())
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
