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
	expectedListing := Path{'#', '.', '#', '.', '#', '#', '#'}
	expectedGroups := []int{1, 1, 3}
	r := NewRecord(knownLines[0], false)
	assert.Equal(t, expectedListing, r.Listing)
	assert.Equal(t, expectedGroups, r.Groups)
}

func TestNConfigs(t *testing.T) {
	expected := []int{1, 4, 1, 1, 4, 10}
	for i, line := range testLines {
		t.Run(line, func(t *testing.T) {
			r := NewRecord(line, false)
			assert.Equal(t, expected[i], r.NPossibleConfigs())
		})
	}
}

func TestNConfigsKnownCase(t *testing.T) {
	for _, line := range knownLines {
		t.Run(line, func(t *testing.T) {
			r := NewRecord(line, false)
			assert.Equal(t, 1, r.NPossibleConfigs())
		})
	}
}

func TestTotalConfigs(t *testing.T) {
	rs := NewRecordSet(testLines, false)
	assert.Equal(t, 21, rs.TotalConfigs())
}

func TestPart1(t *testing.T) {
	lines := utils.ReadInput()
	rs := NewRecordSet(lines, false)
	part1Answer := rs.TotalConfigs()
	assert.Equal(t, 7922, part1Answer)
}

func TestUnfold(t *testing.T) {
	expListing := Path("???.###????.###????.###????.###????.###")
	expGroups := []int{1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3}
	r := NewRecord(testLines[0], true)
	assert.Equal(t, expListing, r.Listing)
	assert.Equal(t, expGroups, r.Groups)
}

func TestNConfigsUnfold(t *testing.T) {
	expected := []int{1, 16384, 1, 16, 2500, 506250}
	for i, line := range testLines {
		t.Run(line, func(t *testing.T) {
			r := NewRecord(line, true)
			assert.Equal(t, expected[i], r.NPossibleConfigs())
		})
	}
}

func TestTotalConfigsUnfold(t *testing.T) {
	rs := NewRecordSet(testLines, true)
	assert.Equal(t, 525152, rs.TotalConfigs())
}

func BenchmarkNconfigs(b *testing.B) {
	for i := 0; i < b.N; i++ {
		rs := NewRecordSet(testLines, true)
		rs.TotalConfigs()
	}
}

func TestPart2(t *testing.T) {
	lines := utils.ReadInput()
	rs2 := NewRecordSet(lines, true)
	part2Answer := rs2.TotalConfigs()
	assert.Equal(t, 18093821750095, part2Answer)
}

func TestHeapPosOnly(t *testing.T) {
	h := NewCursorHeap()
	h.PushH(Cursor{Position: 3})
	h.PushH(Cursor{Position: 2})
	h.PushH(Cursor{Position: 1})
	h.PushH(Cursor{Position: 5})
	h.PushH(Cursor{Position: 0})
	h.PushH(Cursor{Position: 4})

	for i := range 6 {
		assert.Equal(t, i, h.Peek().Position)
		assert.Equal(t, i, h.PopH().Position)
	}
}

func TestHeapGroups(t *testing.T) {
	gs := [][]int{{4}, {1, 3, 5, 7}, {3, 6, 2, 7}, {1, 2, 3, 5, 7}, {1, 2, 3, 5, 7}, {2, 2, 3, 5, 7}}
	h := NewCursorHeap()
	h.PushH(Cursor{Position: 3, RemainingGroups: gs[3]})
	h.PushH(Cursor{Position: 3, RemainingGroups: gs[4]})
	h.PushH(Cursor{Position: 3, RemainingGroups: gs[2]})
	h.PushH(Cursor{Position: 3, RemainingGroups: gs[0]})
	h.PushH(Cursor{Position: 3, RemainingGroups: gs[1]})
	h.PushH(Cursor{Position: 3, RemainingGroups: gs[5]})

	for i := range 6 {
		assert.Equal(t, 3, h.Peek().Position)
		assert.Equal(t, gs[i], h.Peek().RemainingGroups)

		top := h.PopH()
		assert.Equal(t, 3, top.Position)
		assert.Equal(t, gs[i], top.RemainingGroups)
	}
}
