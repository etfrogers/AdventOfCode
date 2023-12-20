package main

import (
	"os"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

var testCase string = `467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..`

var testLines []string = strings.Split(testCase, "\n")

func TestPartNumbersTestCase(t *testing.T) {
	expected := []int{467, 35, 633, 617, 592, 755, 664, 598}
	partNumbers := FindPartNumbers(testLines)
	assert.Equal(t, partNumbers, expected)
}

func TestSumPartNumbers(t *testing.T) {
	expected := 4361
	sum := SumPartNumbers(testLines)
	assert.Equal(t, sum, expected)
}

func TestPart1(t *testing.T) {
	expected := 527144
	doc, err := os.ReadFile("input.txt")
	check(err)
	lines := strings.Split(string(doc), "\n")

	assert.Equal(t, SumPartNumbers(lines), expected)
}
