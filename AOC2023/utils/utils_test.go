package utils

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSplitSliceInt(t *testing.T) {
	testCases := []struct {
		input    []int
		sep      int
		expected [][]int
	}{
		{[]int{1, 2, 3}, 2, [][]int{{1}, {3}}},
		{[]int{}, 2, [][]int{}},
		{[]int{1, 2, 3}, 4, [][]int{{1, 2, 3}}},
		{[]int{1, 2, 3, 4, 5, 6}, 6, [][]int{{1, 2, 3, 4, 5}}},
		{[]int{1, 2, 3, 4, 5, 6}, 1, [][]int{{2, 3, 4, 5, 6}}},
		{[]int{1, 2, 3, 4, 5, 6}, 2, [][]int{{1}, {3, 4, 5, 6}}},
		{[]int{1, 2, 1, 2, 1, 2}, 2, [][]int{{1}, {1}, {1}}},
		{[]int{1, 2, 1, 2, 1, 2}, 1, [][]int{{2}, {2}, {2}}},
		{[]int{1, 1, 1, 1, 1, 1}, 1, [][]int{}},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc.input), func(t *testing.T) {
			assert.Equal(t, tc.expected, SplitSplice(tc.input, tc.sep))
		})
	}
}

func TestSplitSliceString(t *testing.T) {
	testCases := []struct {
		input    []string
		sep      string
		expected [][]string
	}{
		{[]string{"1", "2", "3"}, "2", [][]string{{"1"}, {"3"}}},
		{[]string{}, "2", [][]string{}},
		{[]string{"1", "2", "3"}, "4", [][]string{{"1", "2", "3"}}},
		{[]string{"1", "2", "3", "4", "5", "6"}, "6", [][]string{{"1", "2", "3", "4", "5"}}},
		{[]string{"1", "2", "3", "4", "5", "6"}, "1", [][]string{{"2", "3", "4", "5", "6"}}},
		{[]string{"1", "2", "3", "4", "5", "6"}, "2", [][]string{{"1"}, {"3", "4", "5", "6"}}},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc.input), func(t *testing.T) {
			assert.Equal(t, tc.expected, SplitSplice(tc.input, tc.sep))
		})
	}
}

func TestPowInts(t *testing.T) {
	testCases := []struct {
		n      int
		m      int
		answer int
	}{
		{1, 1, 1},
		{1, 4, 1},
		{1, 1000, 1},
		{2, 2, 4},
		{2, 3, 8},
		{2, 8, 256},
		{0, 8, 0},
		{0, 0, 1},
		{0, 0, 1},
		{-1, 1, -1},
		{-1, 2, 1},
		{-2, 2, 4},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%d, %d", tc.n, tc.m), func(t *testing.T) {
			val, err := PowInts(tc.n, tc.m)
			assert.Nil(t, err)
			assert.Equal(t, tc.answer, val)
		})
	}
}

func TestPowIntsError(t *testing.T) {
	testCases := []struct {
		n int
		m int
	}{
		{1, -11},
		{0, -1},
		{99999090978, -9},
		{0, -1},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%d, %d", tc.n, tc.m), func(t *testing.T) {
			_, err := PowInts(tc.n, tc.m)
			assert.Error(t, err, "n must be >= 0")
		})
	}
}

func TestProd(t *testing.T) {
	testCases := []struct {
		input  []int
		answer int
	}{
		{[]int{0, 1, 1, 3, 789473289}, 0},
		{[]int{1, 1, 1, 1, 1, 1, 1}, 1},
		{[]int{1, 1, 1, 1, 1, 1, 64}, 64},
		{[]int{99999090978}, 99999090978},
		{[]int{0}, 0},
		{[]int{}, 0},
		{[]int{-1, 1, 1, 1, 1, 1, 64}, -64},
		{[]int{-1, -1, 1, 1, 1, 1, 64}, 64},
		{[]int{-1, -1, -1, 1, 1, 1, 64}, -64},
		{[]int{-1, -1, -1, -1, 1, 1, 64}, 64},
		{[]int{-1, -1, -1, -1, -1, 1, 64}, -64},
		{[]int{-1, -1, -1, -1, -1, -1, 64}, 64},
		{[]int{-1, -1, -1, -1, -1, -1, -64}, -64},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc.input), func(t *testing.T) {
			assert.Equal(t, tc.answer, Prod(tc.input))
		})
	}
}

func TestSum(t *testing.T) {
	testCases := []struct {
		input  []int
		answer int
	}{
		{[]int{0, 1, 1, 3, 789473289}, 789473294},
		{[]int{0, 0, 0, 0, 0}, 0},
		{[]int{1, -1, -99, 99}, 0},
		{[]int{1, 1, 1, 1, 1}, 5},
		{[]int{}, 0},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc.input), func(t *testing.T) {
			assert.Equal(t, tc.answer, Sum(tc.input))
		})
	}
}
