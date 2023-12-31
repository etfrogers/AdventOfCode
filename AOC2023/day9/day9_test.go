package main

import (
	"fmt"
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase string = `0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45`

var testLines []string = strings.Split(testCase, "\n")

func TestPart1(t *testing.T) {
	expected := 2008960228
	lines := utils.ReadInput()
	sequences := NewSequenceList(lines)
	_, part1Answer := sequences.SumExtrapolate()
	assert.Equal(t, expected, part1Answer)
}

func TestExtrap(t *testing.T) {
	expectedEnd := []int{18, 28, 68}
	expectedStart := []int{-3, 0, 5}
	for i, line := range testLines {
		t.Run(fmt.Sprint(line), func(t *testing.T) {
			s := NewSequence(line)
			startVal, endVal := s.Extrapolate()
			assert.Equal(t, expectedEnd[i], endVal)
			assert.Equal(t, expectedStart[i], startVal)
		})
	}
}

func TestSumExtrap(t *testing.T) {
	sl := NewSequenceList(testLines)
	expectedEnd := 114
	expectedStart := 2
	startSum, endSum := sl.SumExtrapolate()
	assert.Equal(t, expectedEnd, endSum)
	assert.Equal(t, expectedStart, startSum)
}
