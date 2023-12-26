package main

import (
	"fmt"
	"slices"
	"strings"
	"testing"
	"utils"
	"utils/set"

	"github.com/stretchr/testify/assert"
)

var testCase string = `seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4`

var testLines []string = strings.Split(testCase, "\n")

func TestTestLocationFinder(t *testing.T) {
	expectedLocations := set.New([]int{82, 43, 86, 35}...)
	mapSet := NewMapSet(testLines, false)
	assert.True(t, expectedLocations.Equals(FindLocations(mapSet)))
}

func TestSingleMapping(t *testing.T) {
	testCases := [][]int{
		{79, 81},
		{14, 14},
		{55, 57},
		{13, 13},
	}
	mapSet := NewMapSet(testLines, false)
	seed_map := mapSet.Maps()[0]
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc), func(t *testing.T) {
			assert.Equal(t, tc[1], seed_map.DoMapping(tc[0]))
		})
	}
}

func TestSeeds(t *testing.T) {
	expectedSeeds := set.New[int](79, 14, 55, 13)
	mapSet := NewMapSet(testLines, false)
	assert.True(t, mapSet.(MapSetInts).SeedNumbers.Equals(expectedSeeds))
}

func TestPart1(t *testing.T) {
	expected := 382895070
	lines := utils.ReadInput()
	maps := NewMapSet(lines, false)
	locs := FindLocations(maps)
	part1Answer := slices.Min(locs.Items())
	assert.Equal(t, expected, part1Answer)
}

type entry struct {
	outStart int
	inStart  int
	len      int
}

func TestMaps(t *testing.T) {
	testCases := []struct {
		id      string
		index   int
		entries []entry
	}{
		{"seed-to-soil", 0, []entry{{50, 98, 2}, {52, 50, 48}}},
		{"soil-to-fertilizer", 1, []entry{{0, 15, 37}, {37, 52, 2}, {39, 0, 15}}},
		{"humidity-to-location", 6, []entry{{60, 56, 37}, {56, 93, 4}}},
	}
	mapSet := NewMapSet(testLines, false)
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc.index), func(t *testing.T) {
			locMap := mapSet.Maps()[tc.index]
			assert.Equal(t, tc.id, locMap.Id)
			for i, entry := range tc.entries {
				assert.Equal(t, entry.inStart, locMap.mappings[i].InputStart)
				assert.Equal(t, entry.outStart, locMap.mappings[i].OutputStart)
				assert.Equal(t, entry.len, locMap.mappings[i].Length)
			}
		})
	}
}

func TestPart2TestCase(t *testing.T) {
	mapSet := NewMapSet(testLines, true)
	expected := 46
	input_seed := 82
	assert.Equal(t, expected, MapThroughSet(mapSet, input_seed))
}

func TestPart2MinTestCase(t *testing.T) {
	mapSet := NewMapSet(testLines, true)
	expected := 46
	locs := FindLocations(mapSet)
	loc := slices.Min(locs.Items())
	assert.Equal(t, expected, loc)
}
