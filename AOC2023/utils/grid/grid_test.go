package grid

import (
	"fmt"
	"testing"
	"utils/iter"

	"github.com/stretchr/testify/assert"
)

func TestIterator(t *testing.T) {
	testCases := []struct {
		inv, cm  bool
		expected string
	}{
		{false, false, "ABCD"},
		{true, false, "DCBA"},
		{false, true, "ACBD"},
		{true, true, "DBCA"},
	}
	strs := []string{"AB", "CD"}
	for _, tc := range testCases {
		t.Run(fmt.Sprintf("invert %t, colMajor %t", tc.inv, tc.cm), func(t *testing.T) {
			grid := NewFromStrings(strs)
			actual := iter.ToString(grid.Iterator(tc.inv, tc.cm))
			assert.Equal(t, tc.expected, actual)
		})
	}

}
