package main

import (
	"fmt"
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase string = `...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....`

var testLines []string = strings.Split(testCase, "\n")

var expanded string = `....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......`

func TestPart1(t *testing.T) {
	expected := 10231178
	lines := utils.ReadInput()
	im := NewSpaceImage(lines)
	im.Expand()
	part1Answer := im.SumGalaxyDistances()
	assert.Equal(t, expected, part1Answer)
}

func TestExpansion(t *testing.T) {
	im := NewSpaceImage(testLines)
	im.Expand()
	assert.Equal(t, expanded, im.String())
}

func TestFindGalaxies(t *testing.T) {
	im := NewSpaceImage(testLines)
	im.Expand()
	galaxies := im.FindGalaxies()
	assert.Equal(t, len(galaxies), 9)
	assert.Equal(t, Galaxy{4, 0}, galaxies[0])
	assert.Equal(t, Galaxy{0, 2}, galaxies[2])
	assert.Equal(t, Galaxy{12, 7}, galaxies[5])
}

func TestDistances(t *testing.T) {
	testCases := []struct {
		i1, i2 int
		dist   int
	}{
		{5, 9, 9},
		{1, 7, 15},
		{3, 6, 17},
		{8, 9, 5},
	}
	im := NewSpaceImage(testLines)
	im.Expand()
	galaxies := im.FindGalaxies()
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			g1, g2 := galaxies[tc.i1-1], galaxies[tc.i2-1]
			assert.Equal(t, tc.dist, FindDistance(g1, g2))
		})
	}
}

func TestSumDists(t *testing.T) {
	im := NewSpaceImage(testLines)
	im.Expand()
	expected := 374
	assert.Equal(t, expected, im.SumGalaxyDistances())

}
