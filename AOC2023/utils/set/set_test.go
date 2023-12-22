package set

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNewInts(t *testing.T) {
	testCases := [][]int{
		{1, 2, 3},
		{},
		{12213, 111, 223242, 423781, 2312},
		// {"a", "b", "euwtfewieu", "qqq"},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc), func(t *testing.T) {
			s := New[int](tc...)
			assert.Equal(t, s.Len(), len(tc))
			for _, val := range tc {
				assert.True(t, s.Contains(val))
			}
			assert.Equal(t, len(s.Items()), len(tc))
			for _, val := range s.Items() {
				assert.True(t, s.Contains(val))
			}
		})
	}
}

func TestNewStrings(t *testing.T) {
	testCases := [][]string{
		{"1", "2", "3"},
		{},
		{"a", "b", "euwtfewieu", "qqq"},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc), func(t *testing.T) {
			s := New[string](tc...)
			assert.Equal(t, s.Len(), len(tc))
			for _, val := range tc {
				assert.True(t, s.Contains(val))
			}
			assert.Equal(t, len(s.Items()), len(tc))
			for _, val := range s.Items() {
				assert.True(t, s.Contains(val))
			}
		})
	}
}

func TestAdd(t *testing.T) {
	testCases := []struct {
		original []int
		toAdd    []int
	}{
		{[]int{1, 2, 3}, []int{1000}},
		{[]int{}, []int{67}},
		{[]int{9879, 1265, -456}, []int{75}},
		{[]int{}, []int{3, 5, 6}},
		{[]int{-1, -4, 789}, []int{}},
		{[]int{-1, -4, 789}, []int{12, 687, 2}},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v + %v", tc.original, tc.toAdd), func(t *testing.T) {
			s := New[int](tc.original...)
			require.Equal(t, s.Len(), len(tc.original))
			if len(tc.toAdd) == 1 {
				// Single Element to add
				toAdd := tc.toAdd[0]
				assert.False(t, s.Contains(toAdd))
				s.Add(toAdd)
				assert.True(t, s.Contains(toAdd))
				assert.Equal(t, s.Len(), len(tc.original)+1)
			} else {
				// Multiple (or zero) elements to add
				for _, item := range tc.toAdd {
					assert.False(t, s.Contains(item))
				}
				s.Add(tc.toAdd...)
				for _, item := range tc.toAdd {
					assert.True(t, s.Contains(item))
				}
				assert.Equal(t, s.Len(), len(tc.original)+len(tc.toAdd))
			}
		})
	}
}

func TestRemovePresentElement(t *testing.T) {
	testCases := []struct {
		original []int
		toRemove []int
	}{
		{[]int{1, 2, 3}, []int{3}},
		{[]int{}, []int{}},
		{[]int{9879, 1265, -456}, []int{9879}},
		{[]int{3, 5, 6, 8, 567}, []int{3, 5, 6}},
		{[]int{-1, -4, 789}, []int{-1, -4, 789}},
		{[]int{-1, -4, 789}, []int{-1, 789}},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v + %v", tc.original, tc.toRemove), func(t *testing.T) {
			s := New[int](tc.original...)
			require.Equal(t, s.Len(), len(tc.original))
			if len(tc.toRemove) == 1 {
				// Single Element to remove
				toAdd := tc.toRemove[0]
				assert.True(t, s.Contains(toAdd))
				s.Remove(toAdd)
				assert.False(t, s.Contains(toAdd))
				assert.Equal(t, s.Len(), len(tc.original)-1)
			} else {
				// Multiple (or zero) elements to remove
				for _, item := range tc.toRemove {
					assert.True(t, s.Contains(item))
				}
				s.Remove(tc.toRemove...)
				for _, item := range tc.toRemove {
					assert.False(t, s.Contains(item))
				}
				assert.Equal(t, s.Len(), len(tc.original)-len(tc.toRemove))
			}
		})
	}
}

func TestRemoveMissingElement(t *testing.T) {
	testCases := []struct {
		original []int
		toRemove []int
	}{
		{[]int{1, 2, 3}, []int{4}},
		{[]int{}, []int{4567132, 21213, 122}},
		{[]int{9879, 1265, -456}, []int{987}},
		{[]int{3, 5, 6, 8, 567}, []int{}},
		{[]int{-1, -4, 789}, []int{-1, -4, 1678}},
		{[]int{-1, -4, 789}, []int{-2, 3121}},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v + %v", tc.original, tc.toRemove), func(t *testing.T) {
			s := New[int](tc.original...)
			require.Equal(t, s.Len(), len(tc.original))
			if len(tc.toRemove) == 1 {
				// Single Element to remove
				toAdd := tc.toRemove[0]
				wasPresent := s.Contains(toAdd)
				s.Remove(toAdd)
				assert.False(t, s.Contains(toAdd))
				if wasPresent {
					assert.Equal(t, s.Len(), len(tc.original)-1)
				} else {
					assert.Equal(t, s.Len(), len(tc.original))
				}
			} else {
				// Multiple (or zero) elements to remove
				nPresent := 0
				for _, item := range tc.toRemove {
					if s.Contains(item) {
						nPresent++
					}
				}
				s.Remove(tc.toRemove...)
				for _, item := range tc.toRemove {
					assert.False(t, s.Contains(item))
				}
				assert.Equal(t, s.Len(), len(tc.original)-nPresent)
			}
		})
	}
}

func TestUnion(t *testing.T) {
	testCases := []struct {
		s1          Set[int]
		s2          Set[int]
		expectedSet Set[int]
	}{
		{New[int](1, 2, 3), New[int](4, 5, 6), New[int](1, 2, 3, 4, 5, 6)},
		{New[int](), New[int](4, 5, 6), New[int](4, 5, 6)},
		{New[int](638217, -789, -1, 89012, 21786), New[int](4, 5, 6), New[int](638217, -789, -1, 89012, 21786, 4, 5, 6)},
		{New[int](638217, -789, -1, 89012, 21786), New[int](), New[int](638217, -789, -1, 89012, 21786)},
		{New[int](), New[int](), New[int]()},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v + %v", tc.s1, tc.s2), func(t *testing.T) {
			s := Union(tc.s1, tc.s2)
			assert.True(t, s.Equals(tc.expectedSet))
		})
	}
}

func TestDifference(t *testing.T) {
	testCases := []struct {
		s1          Set[int]
		s2          Set[int]
		expectedSet Set[int]
	}{
		{New[int](1, 2, 3), New[int](4, 5, 6), New[int](1, 2, 3)},
		{New[int](), New[int](4, 5, 6), New[int]()},
		{New[int](4, 5, 6), New[int](4, 5, 6), New[int]()},
		{New[int](638217, -789, -1, 89012, 21786), New[int](), New[int](638217, -789, -1, 89012, 21786)},
		{New[int](), New[int](), New[int]()},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v + %v", tc.s1, tc.s2), func(t *testing.T) {
			s := Difference(tc.s1, tc.s2)
			assert.True(t, s.Equals(tc.expectedSet))
		})
	}
}

func TestIntersection(t *testing.T) {
	testCases := []struct {
		s1          Set[int]
		s2          Set[int]
		expectedSet Set[int]
	}{
		{New[int](1, 2, 3), New[int](4, 5, 6), New[int]()},
		{New[int](), New[int](4, 5, 6), New[int]()},
		{New[int](4, 5, 6), New[int](4, 5, 6), New[int](4, 5, 6)},
		{New[int](4, 5, 6), New[int](4, 5, 7), New[int](4, 5)},
		{New[int](638217, -789, -1, 89012, 21786), New[int](), New[int]()},
		{New[int](), New[int](), New[int]()},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v + %v", tc.s1, tc.s2), func(t *testing.T) {
			s := Intersection(tc.s1, tc.s2)
			assert.True(t, s.Equals(tc.expectedSet))
		})
	}
}

func TestClear(t *testing.T) {
	testCases := [][]string{
		{"1", "2", "3"},
		{},
		{"a", "b", "euwtfewieu", "qqq"},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("%v", tc), func(t *testing.T) {
			s := New[string](tc...)
			for _, item := range tc {
				assert.True(t, s.Contains(item))
			}
			assert.Equal(t, s.Len(), len(tc))
			s.Clear()
			for _, item := range tc {
				assert.False(t, s.Contains(item))
			}
			assert.Equal(t, s.Len(), 0)
		})
	}
}
