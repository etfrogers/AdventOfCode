package iter

import (
	"fmt"
	"math/rand"
	"slices"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

func TestSliceRoundTrip(t *testing.T) {
	testCases := [][]any{
		{},
		{1, 2, 3, 4, 5},
		{1, 1, 1, 1, 1},
		{1},
		{"A", "bhdas", "wewq"},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			assert.Equal(t, tc, ToSlice(FromSlice(tc)))
		})
	}
}

func TestStringRoundTrip(t *testing.T) {
	testCases := []string{
		"",
		"{1, 2, 3, 4, 5}",
		"daqwdq",
		"aaaaaa",
		"121312321112w21",
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			assert.Equal(t, tc, ToString(FromString(tc)))
		})
	}
}

func TestSliceRoundTripRand(t *testing.T) {
	for i := 0; i < 10; i++ {
		t.Run(fmt.Sprint(i), func(t *testing.T) {
			s := utils.RandSlice[int](100, 10000)
			assert.Equal(t, s, ToSlice(FromSlice(s)))

			sf := utils.RandSlice[float64](100, 10000)
			assert.Equal(t, sf, ToSlice(FromSlice(sf)))
		})
	}
}

func intLess(v1, v2 int) bool       { return v1 < v2 }
func floatLess(v1, v2 float64) bool { return v1 < v2 }

func TestMaxMinVsFunc(t *testing.T) {
	for i := 0; i < 10; i++ {
		t.Run(fmt.Sprint(i), func(t *testing.T) {
			s := utils.RandSlice[int](100, 10000)
			assert.Equal(t, Max(FromSlice(s)), MaxFunc(FromSlice(s), intLess))
			assert.Equal(t, Min(FromSlice(s)), MinFunc(FromSlice(s), intLess))

			sf := utils.RandSlice[float64](100, 10000)
			assert.Equal(t, Max(FromSlice(sf)), MaxFunc(FromSlice(sf), floatLess))
			assert.Equal(t, Min(FromSlice(sf)), MinFunc(FromSlice(sf), floatLess))
		})
	}
}

func TestMaxMinEmpty(t *testing.T) {
	emptyIter := FromSlice[int]([]int{})
	assert.Panics(t, func() { Max(emptyIter) })
	emptyIter = FromSlice[int]([]int{})
	assert.Panics(t, func() { Min(emptyIter) })
}

func TestMax(t *testing.T) {
	testCases := []struct {
		input    []int
		expected int
	}{
		{[]int{1, 2, 3, 4, 5}, 5},
		{[]int{1, 1, 1, 1, 1}, 1},
		{[]int{83290}, 83290},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			it := FromSlice(tc.input)
			assert.Equal(t, tc.expected, Max(it))
		})
	}
}

func TestMin(t *testing.T) {
	testCases := []struct {
		input    []int
		expected int
	}{
		{[]int{1, 2, 3, 4, 5}, 1},
		{[]int{1, 1, 1, 1, 1}, 1},
		{[]int{83290}, 83290},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			it := FromSlice(tc.input)
			assert.Equal(t, tc.expected, Min(it))
		})
	}
}

func TestMaxVsSliceRand(t *testing.T) {
	for i := 0; i < 10; i++ {
		t.Run(fmt.Sprint(i), func(t *testing.T) {
			s := utils.RandSlice[int](100, 10000)
			sMax := slices.Max(s)
			iMax := Max(FromSlice(s))
			assert.Equal(t, sMax, iMax)

			sf := utils.RandSlice[float64](100, 10000)
			assert.Equal(t, slices.Max(sf), Max(FromSlice(sf)))
		})
	}
}

func TestMinVsSliceRand(t *testing.T) {
	for i := 0; i < 100; i++ {
		t.Run(fmt.Sprint(i), func(t *testing.T) {
			s := utils.RandSlice[int](100, 10000)
			assert.Equal(t, slices.Min(s), Min(FromSlice(s)))

			sf := utils.RandSlice[float64](100, 10000)
			assert.Equal(t, slices.Min(sf), Min(FromSlice(sf)))
		})
	}
}

func TestChain(t *testing.T) {
	testCases := []struct {
		inputs   [][]int
		expected []int
	}{
		{[][]int{{}, {}, {}}, []int{}},
		{[][]int{{1}, {2}, {3}}, []int{1, 2, 3}},
		{[][]int{{1}, {}, {3}}, []int{1, 3}},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			its := utils.Map(tc.inputs, FromSlice)
			chainedIt := Chain(its...)
			actual := ToSlice(chainedIt)
			assert.Equal(t, tc.expected, actual)
		})
	}
}

func TestChainAgainstAppendRandom(t *testing.T) {
	for i := 0; i < 100; i++ {
		t.Run(fmt.Sprint(i), func(t *testing.T) {
			lengthIts := rand.Intn(10)
			inputs := make([][]float64, lengthIts)
			lens := make([]int, lengthIts)
			for i := range inputs {
				lens[i] = rand.Intn(1000)
				inputs[i] = utils.RandSlice[float64](lens[i], 1000000)
			}
			its := utils.Map(inputs, FromSlice)
			chainedIt := Chain(its...)
			actual := ToSlice(chainedIt)

			expected := make([]float64, 0, utils.Sum(lens))
			for _, input := range inputs {
				expected = append(expected, input...)
			}

			assert.Equal(t, expected, actual)
		})
	}
}

func TestMap(t *testing.T) {
	ints := []int{0, 1, 2, 3}
	expected := []int{0, 1, 4, 9}
	output := Map(func(i int) int { x, _ := utils.PowInts(i, 2); return x }, FromSlice(ints))
	assert.Equal(t, expected, ToSlice(output))

	expected_s := []string{"0", "1", "2", "3"}
	output_s := Map(func(i int) string { return fmt.Sprint(i) }, FromSlice(ints))
	assert.Equal(t, expected_s, ToSlice(output_s))

	// regenerate as it has been consumed
	output_s = Map(func(i int) string { return fmt.Sprint(i) }, FromSlice(ints))
	output = Map(func(s string) int { return utils.AtoiError(s) }, output_s)
	assert.Equal(t, ints, ToSlice(output))
}

func add[T int | float64](x, y T) T {
	return x + y
}

func TestReduceAgainstSumInt(t *testing.T) {
	for i := 0; i < 10; i++ {
		t.Run(fmt.Sprintf("%d", i), func(t *testing.T) {
			length := rand.Intn(100) + 2
			s := utils.RandSlice[int](length, 1000)
			sum := utils.Sum(s)
			reduceSum := Reduce(add, FromSlice(s), 0)
			assert.Equal(t, sum, reduceSum)
		})
	}
}

func TestReduceAgainstSumFloat(t *testing.T) {
	for i := 0; i < 10; i++ {
		t.Run(fmt.Sprintf("%d", i), func(t *testing.T) {
			length := rand.Intn(100) + 2
			s := utils.RandSlice[float64](length, 1000)
			sum := utils.Sum(s)
			reduceSum := Reduce(add, FromSlice(s), 0)
			assert.Equal(t, sum, reduceSum)
		})
	}
}

func TestEquals(t *testing.T) {
	testCases := [][]int{
		{},
		{1, 2, 3, 4, 5},
		{1, 1, 1, 1, 1},
		{1},
	}
	for i, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			it := FromSlice(tc)
			itEq := FromSlice(tc)
			nextI := (i + 1) % len(testCases)
			itNeq := FromSlice(testCases[nextI])

			assert.True(t, Equal(it, itEq))
			// reset it
			it = FromSlice(tc)
			assert.False(t, Equal(it, itNeq))
		})
	}
}
