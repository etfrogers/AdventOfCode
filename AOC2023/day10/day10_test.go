package main

import (
	"fmt"
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase1plain string = `.....
.S-7.
.|.|.
.L-J.
.....`

var testCase1real string = `-L|F7
7S-7|
L|7||
-L-J|
L|-JF`

var testCase2plain string = `..F7.
.FJ|.
SJ.L7
|F--J
LJ...`

var testCase2real string = `7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ`

var testCases []string = []string{testCase1plain, testCase1real, testCase2plain, testCase2real}

var testCaseLines [][]string = utils.Map(testCases, func(s string) []string { return strings.Split(s, "\n") })

func TestPart1(t *testing.T) {
	expected := 6640
	lines := utils.ReadInput()
	p := NewPipeline(lines)
	part1Answer := p.MaxDistFromStart()
	assert.Equal(t, expected, part1Answer)
}

func TestMaxDist(t *testing.T) {
	expectedDist := []int{4, 4, 8, 8}
	for i, lines := range testCaseLines {
		t.Run(fmt.Sprint(lines), func(t *testing.T) {
			pipes := NewPipeline(lines)
			assert.Equal(t, expectedDist[i], pipes.MaxDistFromStart())
		})
	}
}
