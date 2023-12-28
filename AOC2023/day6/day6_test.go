package main

import (
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase string = `Time:      7  15   30
Distance:  9  40  200`

var testLines []string = strings.Split(testCase, "\n")

func TestPart1(t *testing.T) {
	expected := 170000
	lines := utils.ReadInput()
	races := NewRaces(lines, false)
	nWinners := utils.Map(races, func(x Race) int { return x.NWinners() })
	part1Answer := utils.Prod(nWinners)
	assert.Equal(t, expected, part1Answer)
}

func TestDistances(t *testing.T) {
	expectedTimes := []int{0, 1, 2, 3, 4, 5, 6, 7}
	expectedDists := []int{0, 6, 10, 12, 12, 10, 6, 0}
	races := NewRaces(testLines, false)
	assert.Equal(t, 3, len(races))
	results := races[0].PossibleResults()
	assert.Equal(t, 8, len(results))
	for i, result := range results {
		assert.Equal(t, expectedTimes[i], result.holdTime)
		assert.Equal(t, expectedDists[i], result.achievedDistance)
	}
}

func TestWays(t *testing.T) {
	expectedWays := []int{4, 8, 9}
	races := NewRaces(testLines, false)
	assert.Equal(t, 3, len(races))
	winners := utils.Map(races, func(x Race) int { return x.NWinners() })
	assert.Equal(t, expectedWays, winners)
}

func TestBadKerning(t *testing.T) {
	races := NewRaces(testLines, true)
	race := races[0]
	assert.Equal(t, 71530, race.time)
	assert.Equal(t, 940200, race.recordDistance)
}

func TestPart2WinnersTestCase(t *testing.T) {
	expectedWays := 71503
	races := NewRaces(testLines, true)
	winners := races[0].NWinners()
	assert.Equal(t, expectedWays, winners)
}

func TestPart2(t *testing.T) {
	expectedWays := 20537782
	lines := utils.ReadInput()
	races := NewRaces(lines, true)
	winners := races[0].NWinners()
	assert.Equal(t, expectedWays, winners)
}
