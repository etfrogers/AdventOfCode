package main

import (
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase string = `...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........`

var testLines []string = strings.Split(testCase, "\n")

func TestStart(t *testing.T) {
	g := NewGarden(testLines)
	assert.Equal(t, 5, g.start.x)
	assert.Equal(t, 5, g.start.y)
}

func TestSteps(t *testing.T) {
	g := NewGarden(testLines)
	s := g.FindStepOutcomes(6)
	assert.Equal(t, 16, s)
}

func TestPart1(t *testing.T) {
	lines := utils.ReadInput()
	g := NewGarden(lines)
	part1Answer := g.FindStepOutcomes(64)
	assert.Equal(t, 3600, part1Answer)
}
