package utils

import (
	"fmt"
	"math/rand"
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
			assert.Equal(t, tc.expected, SplitSlice(tc.input, tc.sep))
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
			assert.Equal(t, tc.expected, SplitSlice(tc.input, tc.sep))
		})
	}
}

func TestCutSliceInt(t *testing.T) {
	testCases := []struct {
		input     []int
		sep       int
		expected1 []int
		expected2 []int
	}{
		{[]int{1, 2, 1}, 2, []int{1}, []int{1}},
		{[]int{1, 2, 2, 1}, 2, []int{1}, []int{2, 1}},
		{[]int{1, 1, 1, 1}, 2, []int{1, 1, 1, 1}, []int{}},
		{[]int{1, 1, 1, 1}, 1, []int{}, []int{1, 1, 1}},
		{[]int{}, 2, []int{}, []int{}},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			p1, p2 := CutSlice(tc.input, tc.sep)
			assert.Equal(t, tc.expected1, p1)
			assert.Equal(t, tc.expected2, p2)
		})
	}
}

func TestCutSliceString(t *testing.T) {
	testCases := []struct {
		input     []string
		sep       string
		expected1 []string
		expected2 []string
	}{
		{[]string{"1", "2", "1"}, "2", []string{"1"}, []string{"1"}},
		{[]string{"1", "2", "2", "1"}, "2", []string{"1"}, []string{"2", "1"}},
		{[]string{"1", "1", "1", "1"}, "2", []string{"1", "1", "1", "1"}, []string{}},
		{[]string{"1", "1", "1", "1"}, "1", []string{}, []string{"1", "1", "1"}},
		{[]string{}, "2", []string{}, []string{}},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			p1, p2 := CutSlice(tc.input, tc.sep)
			assert.Equal(t, tc.expected1, p1)
			assert.Equal(t, tc.expected2, p2)
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

func randSlice[T int | float64](length int, max int) []T {
	var dummy T
	result := make([]T, length)
	for i := 0; i < length; i++ {
		switch any(dummy).(type) {
		case int, string:
			if max == 0 {
				result[i] = T(rand.Int())
			} else {
				result[i] = T(rand.Intn(max))
			}
		case float64:
			if max == 0 {
				result[i] = T(rand.Float64())
			} else {
				result[i] = T(rand.Float64() * float64(max))
			}
		}

	}
	return result
}

func add[T float64 | int | string](x, y T) T {
	return x + y
}

func TestReduceAgainstSumInt(t *testing.T) {
	for i := 0; i < 10; i++ {
		t.Run(fmt.Sprintf("%d", i), func(t *testing.T) {
			length := rand.Intn(100) + 2
			s := randSlice[int](length, 1000)
			sum := Sum(s)
			reduceSum := Reduce[int](s, add)
			assert.Equal(t, sum, reduceSum)
		})
	}
}

func TestReduceAgainstSumFloat(t *testing.T) {
	for i := 0; i < 10; i++ {
		t.Run(fmt.Sprintf("%d", i), func(t *testing.T) {
			length := rand.Intn(100) + 2
			s := randSlice[float64](length, 1000)
			sum := Sum(s)
			reduceSum := Reduce(s, add)
			assert.Equal(t, sum, reduceSum)
		})
	}
}

func TestReduceError(t *testing.T) {
	for i := 0; i < 10; i++ {
		t.Run(fmt.Sprintf("%d", i), func(t *testing.T) {
			// panic len 0
			testFn := func() { Reduce([]int{}, add) }
			assert.Panics(t, testFn)
			// panic len 1
			testFn = func() { Reduce([]int{1}, add) }
			assert.Panics(t, testFn)
			// no panic len 2
			testFn = func() { Reduce([]int{1, 2}, add) }
			testFn()

		})
	}
}

func TestAll(t *testing.T) {
	testCases := []struct {
		input    []bool
		expected bool
	}{
		{[]bool{true}, true},
		{[]bool{}, true},
		{[]bool{true, true, true}, true},
		{[]bool{true, true, false}, false},
		{[]bool{false, false, false}, false},
		{[]bool{false}, false},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			assert.Equal(t, tc.expected, All(tc.input))
		})
	}
}

func TestAny(t *testing.T) {
	testCases := []struct {
		input    []bool
		expected bool
	}{
		{[]bool{true}, true},
		{[]bool{}, false},
		{[]bool{true, true, true}, true},
		{[]bool{true, true, false}, true},
		{[]bool{false, false, false}, false},
		{[]bool{false}, false},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			assert.Equal(t, tc.expected, Any(tc.input))
		})
	}
}

func TestGCF(t *testing.T) {
	testCases := []struct {
		input    []int
		expected int
	}{
		{[]int{}, 0},
		{[]int{1}, 1},
		{[]int{987}, 987},
		{[]int{1071, 462}, 21},
		{[]int{462, 1071}, 21},
		{[]int{1386, 3213}, 63},
		{[]int{3213, 1386}, 63},
		{[]int{2, 2, 2, 2, 2}, 2},
		{[]int{2, 4, 6, 8, 10}, 2},
		{[]int{45, 100, 25, 15, 10}, 5},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			assert.Equal(t, tc.expected, GCF(tc.input...))
		})
	}
}

func TestLCM(t *testing.T) {
	testCases := []struct {
		input    []int
		expected int
	}{
		{[]int{}, 0},
		{[]int{1}, 1},
		{[]int{987}, 987},
		{[]int{6, 10}, 30},
		{[]int{10, 6}, 30},
		{[]int{10, 18, 25}, 450},
		{[]int{18, 25, 10}, 450},
		{[]int{10, 12, 15, 75}, 300},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			assert.Equal(t, tc.expected, LCM(tc.input...))
		})
	}
}
