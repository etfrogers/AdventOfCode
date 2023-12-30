package main

import (
	"fmt"
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase1 string = `RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)`

var testCase2 string = `LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)`

var testLines1 []string = strings.Split(testCase1, "\n")
var testLines2 []string = strings.Split(testCase2, "\n")

func TestPart1(t *testing.T) {
	expected := 16897
	lines := utils.ReadInput()
	inst, net := NewNetwork(lines)
	part1Answer := net.Walk(inst)
	assert.Equal(t, expected, part1Answer)
}

func TestExampleWalk(t *testing.T) {
	testCases := []struct {
		lines      []string
		walkLength int
	}{
		{testLines1, 2},
		{testLines2, 6},
	}
	for _, tc := range testCases {
		t.Run(fmt.Sprint(tc), func(t *testing.T) {
			instructions, net := NewNetwork(tc.lines)
			walkLength := net.Walk(instructions)
			assert.Equal(t, tc.walkLength, walkLength)
		})
	}
}

func TestGhostWalk(t *testing.T) {
	lines := strings.Split(`LR

	11A = (11B, XXX)
	11B = (XXX, 11Z)
	11Z = (11B, XXX)
	22A = (22B, XXX)
	22B = (22C, 22C)
	22C = (22Z, 22Z)
	22Z = (22B, 22B)
	XXX = (XXX, XXX)`, "\n")
	expected := 6
	inst, net := NewNetwork(lines)

	walkLength := net.GhostWalk(inst)
	assert.Equal(t, expected, walkLength)
}

func TestPart2(t *testing.T) {
	expected := 16563603485021
	lines := utils.ReadInput()
	inst, net := NewNetwork(lines)
	part2Answer := net.GhostWalk(inst)
	assert.Equal(t, expected, part2Answer)
}
