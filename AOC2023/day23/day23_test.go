package main

import (
	"slices"
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase string = `#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#`

var testLines []string = strings.Split(testCase, "\n")

func TestAllPaths(t *testing.T) {
	expected := []int{94, 90, 86, 82, 82, 74}
	tr := NewTrails(testLines)
	lens := tr.PossiblePathLengths()
	slices.Sort(lens)
	slices.Reverse(lens)
	assert.Equal(t, expected, lens)
}

func TestLongestPaths(t *testing.T) {
	expected := 94
	tr := NewTrails(testLines)
	len := tr.LongestPath()
	assert.Equal(t, expected, len)
}

func TestPart1(t *testing.T) {
	expected := 2230
	lines := utils.ReadInput()
	tr := NewTrails(lines)
	part1Answer := tr.LongestPath()
	assert.Equal(t, expected, part1Answer)
}
