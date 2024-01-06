package main

import (
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase string = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

var expectedHashes []int = []int{30, 253, 97, 47, 14, 180, 9, 197, 48, 214, 231}

func TestHash(t *testing.T) {
	assert.Equal(t, Hash("HASH"), 52)
}

func TestCaseHashes(t *testing.T) {
	hashes := HashSlice(testCase)
	assert.Equal(t, expectedHashes, hashes)
}

func TestChecksum(t *testing.T) {
	expected := 1320
	assert.Equal(t, expected, Checksum(testCase))
}

func TestLenses(t *testing.T) {
	expected := []Lens{
		{0, 1, "rn", 1},
		{0, 2, "cm", 2},
		{3, 1, "ot", 7},
		{3, 2, "ab", 5},
		{3, 3, "pc", 6},
	}
	boxes := FollowManual(testCase)
	lenses := GetLenses(boxes)
	assert.Equal(t, expected, lenses)
}

func TestPowers(t *testing.T) {
	expected := []int{1, 4, 28, 40, 72}
	boxes := FollowManual(testCase)
	powers := FocusingPowers(boxes)
	assert.Equal(t, powers, expected)
}

func TestTotalPower(t *testing.T) {
	boxes := FollowManual(testCase)
	assert.Equal(t, 145, TotalPower(boxes))
}

func TestPart1(t *testing.T) {
	input := utils.ReadInput()[0]
	part1Answer := Checksum(input)
	assert.Equal(t, 507291, part1Answer)
}

func TestPart2(t *testing.T) {
	input := utils.ReadInput()[0]
	boxes := FollowManual(input)
	part2Answer := TotalPower(boxes)
	assert.Equal(t, 296921, part2Answer)
}
