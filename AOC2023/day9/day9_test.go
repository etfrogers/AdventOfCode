package main

import (
	"fmt"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

var testCase string = `0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45`

var testLines []string = strings.Split(testCase, "\n")

func TestPart1(t *testing.T) {
	t.Skip("not implemented")
	assert.Fail(t, "not implemented")
}

func TestExtrap(t *testing.T) {
	expected := []int{18, 28, 68}
	for i, line := range testLines {
		t.Run(fmt.Sprint(line), func(t *testing.T) {
			s := NewSequence(line)
			val := s.Extrapolate()
			assert.Equal(t, expected[i], val)
		})
	}
}

func TestSumExtrap(t *testing.T) {
	sl := NewSequenceList(testLines)
	expected := 114
	assert.Equal(t, expected, sl.SumExtrapolate())
}
