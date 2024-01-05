package main

import (
	"fmt"
	"slices"
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
	im := NewSpaceImage(lines, 2)
	part1Answer := im.SumGalaxyDistances()
	assert.Equal(t, expected, part1Answer)
}

func TestExpansion(t *testing.T) {
	im := NewSpaceImage(testLines, 2)
	assert.Equal(t, expanded, im.String())
}

func TestFindGalaxies(t *testing.T) {
	im := NewSpaceImage(testLines, 2)
	galaxies := im.FindGalaxies()
	assert.Equal(t, len(galaxies), 9)
	assert.Equal(t, Galaxy{3, 0}, galaxies[0])
	assert.Equal(t, Galaxy{0, 2}, galaxies[2])
	assert.Equal(t, Galaxy{9, 6}, galaxies[5])
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
		{1, 4, 9},
		{3, 7, 17},
		{4, 5, 8},
		{5, 4, 8},
	}
	im := NewSpaceImage(testLines, 2)
	galaxies := im.FindGalaxies()
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			g1, g2 := galaxies[tc.i1-1], galaxies[tc.i2-1]
			assert.Equal(t, tc.dist, im.FindDistance(g1, g2))
		})
	}
}

func TestExpLocations(t *testing.T) {
	im := NewSpaceImage(testLines, 2)
	expectedLocsX := []int{2, 5, 8}
	expectedLocsY := []int{3, 7}

	actualX := im.expX.Items()
	slices.Sort(actualX)
	assert.Equal(t, expectedLocsX, actualX)

	actualY := im.expY.Items()
	slices.Sort(actualY)
	assert.Equal(t, expectedLocsY, actualY)
}

func TestSumDists(t *testing.T) {
	testCases := []struct {
		expansion   int
		expectedSum int
	}{
		{2, 374},
		{10, 1030},
		{100, 8410},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			im := NewSpaceImage(testLines, tc.expansion)
			assert.Equal(t, tc.expectedSum, im.SumGalaxyDistances())
		})
	}
}
