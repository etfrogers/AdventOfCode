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
	r := NewRecord(knownLines[0])
	assert.Equal(t, expectedListing, r.Listing)
	assert.Equal(t, expectedGroups, r.Groups)
}

func TestGroups(t *testing.T) {
	for _, line := range knownLines {
		t.Run(line, func(t *testing.T) {
			r := NewRecord(line)
			assert.Equal(t, r.Groups, r.CalculateGroups())
		})
	}
}

func TestGroupsUnknown(t *testing.T) {
	for _, line := range testLines {
		t.Run(line, func(t *testing.T) {
			r := NewRecord(line)
			assert.Equal(t, []int{}, r.CalculateGroups())
		})
	}
}

func TestBuildTree(t *testing.T) {
	expected := []int{8, 32, 256, 16, 16, 512}
	for i, line := range testLines {
		t.Run(line, func(t *testing.T) {
			r := NewRecord(line)
			tree := r.buildTree()
			assert.Equal(t, expected[i], len(tree.GetLeaves()))
		})
	}
}

func TestNConfigs(t *testing.T) {
	expected := []int{1, 4, 1, 1, 4, 10}
	for i, line := range testLines {
		t.Run(line, func(t *testing.T) {
			r := NewRecord(line)
			assert.Equal(t, expected[i], len(r.PossibleConfigs()))
		})
	}
}

func TestTotalConfigs(t *testing.T) {
	rs := NewRecordSet(testLines)
	assert.Equal(t, 21, rs.TotalConfigs())
}

func TestPart(t *testing.T) {
	lines := utils.ReadInput()
	rs := NewRecordSet(lines)
	part1Answer := rs.TotalConfigs()
	assert.Equal(t, 7922, part1Answer)
}
