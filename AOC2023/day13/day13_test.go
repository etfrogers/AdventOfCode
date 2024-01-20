package main

import (
	"strings"
	"testing"
	"utils"
	"utils/grid"

	"github.com/stretchr/testify/assert"
)

var testCase string = `#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

..####..##..##..#
...#..##.####.##.
.##.#.##..##..##.
...#..##.####.##.
.##..#..#....#..#
##.##.##########.
#########.##.####

###.##.##
##.####.#
##.#..#.#
####..###
....##...
##.#..#.#
...#..#..
##..###.#
##......#
##......#
..#.##.#.
...#..#..
##.####.#
....##...
...####..
....##...
##.####.#


.##.##...##...##.
#####..##..##..##
.....##..##..##..
.##.#.#.####.#.#.
.##...#.#..#.#...
....#..........#.
#..#..#......#..#
....###.....####.
.##...#.#..#.#...
.....#..####..#..
#..#...##..##...#
....#...#..#...#.
#..#.##########.#
#..##...####...##
#####.##.##.##.##

#..###.#.
.##..##..
...#.##.#
#..#..###
#..#..###
...#.##.#
###..##..
#..###.#.
.#.#####.
#..##.#..
.#.#.#...
.#.#.#.##
###.#..##
##...##.#
##...##.#

##..###....
##..###....
..#.#.###..
.#..#.#..#.
#####...#..
.....#####.
...#.#.####
`

var testCase2 string = `#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

.#.##.#.#
.##..##..
.#.##.#..
#......##
#......##
.#.##.#..
.##..##.#

#..#....#
###..##..
.##.#####
.##.#####
###..##..
#..#....#
#..##...#

#.##..##.
..#.##.#.
##..#...#
##...#..#
..#.##.#.
..##..##.
#.#.##.#.
`

var testLines []string = strings.Split(testCase, "\n")
var testPatterns []Pattern = BuildPatterns(testLines)
var testPatterns2 []Pattern = BuildPatterns(strings.Split(testCase2, "\n"))

func TestFindReflections(t *testing.T) {
	testCases := []struct {
		direction   Direction
		indexBefore int
	}{
		{vert, 5},
		{horz, 4},
		{vert, 11},
		{vert, 1},
		{vert, 2},
		{horz, 14},
		{horz, 1},
	}
	for i, tc := range testCases {
		reflection := testPatterns[i].FindReflection(false)
		assert.Equal(t, tc.direction, reflection.direction)
		assert.Equal(t, tc.indexBefore, reflection.indexBefore)
	}
}

func TestEdgeCases(t *testing.T) {
	p := Pattern{grid.NewFromStrings([]string{"#..", "..."})}
	ref := p.FindReflection(false)
	assert.Equal(t, Reflection{vert, 2}, ref)

	p = Pattern{grid.NewFromStrings([]string{".##.", "####"})}
	ref = p.FindReflection(false)
	assert.Equal(t, Reflection{vert, 2}, ref)
}

func TestSummarize(t *testing.T) {
	// Only the first two patterns were in in the original example.
	total := Summarize(testPatterns[:2], false)
	assert.Equal(t, 405, total)
}

func TestSummarize2(t *testing.T) {
	total := Summarize(testPatterns2, false)
	assert.Equal(t, 709, total)
}

func TestPart1(t *testing.T) {
	expected := 29846
	lines := utils.ReadInput()
	patterns := BuildPatterns(lines)
	part1Answer := Summarize(patterns, false)
	assert.Equal(t, expected, part1Answer)
}

func TestSmudgeSummarize(t *testing.T) {
	total := Summarize(testPatterns[:2], true)
	assert.Equal(t, 400, total)
}
