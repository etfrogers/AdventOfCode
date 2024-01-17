package counter

import (
	"fmt"
	"testing"
	"utils/iter"

	"github.com/stretchr/testify/assert"
)

func TestCountStringsLen(t *testing.T) {
	testCases := []struct {
		input       string
		expectedLen int
	}{
		{"AAAA", 1},
		{"AAAC", 2},
		{"AGH", 3},
		{"", 0},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc), func(t *testing.T) {
			counter := FromString(tc.input)
			assert.Equal(t, tc.expectedLen, counter.Len())
		})
	}
}

func TestCountIntLen(t *testing.T) {
	testCases := []struct {
		input       []int
		expectedLen int
	}{
		{[]int{1, 1, 1, 1}, 1},
		{[]int{1, 1, 1, 678}, 2},
		{[]int{1, 1, 23, 3}, 3},
		{[]int{}, 0},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc), func(t *testing.T) {
			counter := New(tc.input...)
			assert.Equal(t, tc.expectedLen, counter.Len())
		})
	}
}

func TestCountStrings(t *testing.T) {
	testCases := []struct {
		input          string
		expectedKeys   []string
		expectedCounts []int
	}{
		{"AAAA", []string{"A"}, []int{4}},
		{"AAAC", []string{"A", "C"}, []int{3, 1}},
		{"Agh", []string{"A", "g", "h"}, []int{1, 1, 1}},
		{"", []string{}, []int{}},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc), func(t *testing.T) {
			counter := FromString(tc.input)
			keys, counts := counter.KeysInOrder()
			assert.Equal(t, tc.expectedKeys, keys)
			assert.Equal(t, tc.expectedCounts, counts)
			for i, key := range tc.expectedKeys {
				assert.Equal(t, tc.expectedCounts[i], counter.Get(key))
			}
		})
	}
}

func TestDelete(t *testing.T) {
	counter := FromString("AAABBC")
	keys, counts := counter.KeysInOrder()
	assert.Equal(t, 2, counter.Get("B"))
	assert.Equal(t, []string{"A", "B", "C"}, keys)
	assert.Equal(t, []int{3, 2, 1}, counts)

	counter.Delete("B")
	keys, counts = counter.KeysInOrder()
	assert.Equal(t, 0, counter.Get("B"))
	assert.Equal(t, []string{"A", "C"}, keys)
	assert.Equal(t, []int{3, 1}, counts)

	assert.Equal(t, 3, counter.Get("A"))
	counter.Delete("A")
	keys, counts = counter.KeysInOrder()
	assert.Equal(t, 0, counter.Get("A"))
	assert.Equal(t, []string{"C"}, keys)
	assert.Equal(t, []int{1}, counts)

}

func TestCountInt(t *testing.T) {
	testCases := []struct {
		input          []int
		expectedKeys   []int
		expectedCounts []int
	}{
		{[]int{1, 1, 1, 1}, []int{1}, []int{4}},
		{[]int{1, 1, 1, 678}, []int{1, 678}, []int{3, 1}},
		{[]int{1, 1, 23, 3}, []int{1, 23, 3}, []int{2, 1, 1}},
		{[]int{}, []int{}, []int{}},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc), func(t *testing.T) {
			counter := New(tc.input...)
			keys, counts := counter.KeysInOrder()
			assert.Equal(t, tc.expectedKeys, keys)
			assert.Equal(t, tc.expectedCounts, counts)
			for i, key := range tc.expectedKeys {
				assert.Equal(t, tc.expectedCounts[i], counter.Get(key))
			}
		})
	}
}

func TestIterAgainstFromString(t *testing.T) {
	testCases := []string{
		"AAAA",
		"FDSADEWRTEWASCSADWQEDAFRFTR",
		"",
		"2136735217615555555",
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc), func(t *testing.T) {
			cStr := FromString(tc)
			cIter := FromIter(iter.FromString(tc))
			assert.Equal(t, cStr, cIter)
		})
	}
}

func TestIterAgainstSlice(t *testing.T) {
	testCases := [][]int{
		{1, 23, 2, 54, 2, 2, 2, 2},
		{1, 1, 1, 1, 1},
		{},
		{32121321, 321312, 11, 1, 132, 11, 2},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc), func(t *testing.T) {
			cStr := New(tc...)
			cIter := FromIter(iter.FromSlice(tc))
			assert.Equal(t, cStr, cIter)
		})
	}
}
