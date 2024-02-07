package main

import (
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase string = `???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1`

var knownTestCase = `#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1`

var testLines []string = strings.Split(testCase, "\n")
var knownLines []string = strings.Split(knownTestCase, "\n")

func TestBuild(t *testing.T) {
	expectedListing := []rune{'#', '.', '#', '.', '#', '#', '#'}
	expectedGroups := []int{1, 1, 3}
	r := NewRecord(knownLines[0], false)
	assert.Equal(t, expectedListing, r.Listing)
	assert.Equal(t, expectedGroups, r.Groups)
}

func TestGroups(t *testing.T) {
	for _, line := range knownLines {
		t.Run(line, func(t *testing.T) {
			r := NewRecord(line, false)
			assert.Equal(t, r.Groups, r.CalculateGroups())
		})
	}
}

func TestGroupsUnknown(t *testing.T) {
	for _, line := range testLines {
		t.Run(line, func(t *testing.T) {
			r := NewRecord(line, false)
			assert.Equal(t, []int{}, r.CalculateGroups())
		})
	}
}

func TestNConfigs(t *testing.T) {
	expected := []int{1, 4, 1, 1, 4, 10}
	for i, line := range testLines {
		t.Run(line, func(t *testing.T) {
			r := NewRecord(line, false)
			assert.Equal(t, expected[i], len(r.PossibleConfigs()))
		})
	}
}

func TestTotalConfigs(t *testing.T) {
	rs := NewRecordSet(testLines, false)
	assert.Equal(t, 21, rs.TotalConfigs())
}

func TestPart(t *testing.T) {
	lines := utils.ReadInput()
	rs := NewRecordSet(lines, false)
	part1Answer := rs.TotalConfigs()
	assert.Equal(t, 7922, part1Answer)
}

func TestUnfold(t *testing.T) {
	expListing := []rune("???.###????.###????.###????.###????.###")
	expGroups := []int{1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3}
	r := NewRecord(testLines[0], true)
	assert.Equal(t, expListing, r.Listing)
	assert.Equal(t, expGroups, r.Groups)
}

/*
???.### 1,1,3 - 1 arrangement
.??..??...?##. 1,1,3 - 16384 arrangements
?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
????.#...#... 4,1,1 - 16 arrangements
????.######..#####. 1,6,5 - 2500 arrangements
?###???????? 3,2,1 - 506250 arrangements
*/
func TestNConfigsUnfold(t *testing.T) {
	expected := []int{1, 16384, 1, 16, 2500, 506250}
	for i, line := range testLines {
		t.Run(line, func(t *testing.T) {
			r := NewRecord(line, true)
			assert.Equal(t, expected[i], len(r.PossibleConfigs()))
		})
	}
}
