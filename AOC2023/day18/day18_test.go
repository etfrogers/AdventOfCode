package main

import (
	"fmt"
	"strings"
	"testing"
	"utils"

	"github.com/stretchr/testify/assert"
)

var testCase string = `R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)`

var testLines []string = strings.Split(testCase, "\n")

func TestWalkLen(t *testing.T) {
	is := BuildInstructions(testLines)
	tr := is.Walk()
	assert.Equal(t, 38, len(tr))
}

func TestFilledArea(t *testing.T) {
	is := BuildInstructions(testLines)
	tr := is.Walk()
	im := tr.buildImage()
	area := tr.FilledArea(im)
	printImage(im)
	assert.Equal(t, 62, area)
}

var manualTests = []struct {
	expectedArea int
	instructions string
}{
	{16, `R 3
D 3
L 1
U 2
L 1
D 2
L 1
U 3`},
	{20, `R 5
D 3
L 1
U 2
L 3
D 2
L 1
U 3`},
	{22, `R 5
D 3
L 2
U 2
L 2
D 2
L 1
U 3`},
	{22, `L 5
U 3
R 2
D 2
R 2
U 2
R 1
D 3`},
	{27, `R 2
U 2
R 2
D 2
R 2
D 2
L 6
U 2`},
	{27, `U 1
R 2
U 2
R 2
D 2
R 2
D 2
L 6
U 1`},
	{39, `R 8
D 4
L 2
U 2
L 4
D 2
L 2
U 4`},
}

func appendColor(line string) string {
	return line + " (#000000)"
}

func TestManual(t *testing.T) {
	for i, test := range manualTests {
		t.Run(fmt.Sprint(i), func(t *testing.T) {
			lines := utils.Map(strings.Split(test.instructions, "\n"), appendColor)
			is := BuildInstructions(lines)
			tr := is.Walk()
			im := tr.buildImage()
			expectedSquares := utils.Sum(utils.Map(is, func(i Instruction) int { return i.len }))
			assert.Equal(t, expectedSquares, len(tr))
			area := tr.FilledArea(im)
			printImage(im)
			assert.Equal(t, test.expectedArea, area)
		})
	}
}

func TestShoelace(t *testing.T) {
	is := BuildInstructions(testLines)
	area := ShoelaceTrapezoid(is)
	assert.Equal(t, 62, area)
}

func TestManualShoelace(t *testing.T) {
	for i, test := range append(shoelaceTests, manualTests...) {
		t.Run(fmt.Sprint(i), func(t *testing.T) {
			lines := utils.Map(strings.Split(test.instructions, "\n"), appendColor)
			is := BuildInstructions(lines)
			area := ShoelaceTrapezoid(is)
			assert.Equal(t, test.expectedArea, area)
			tr := is.Walk()
			tr.Render()
		})
	}
}

var shoelaceTests = []struct {
	expectedArea int
	instructions string
}{
	{16, `R 3
D 3
L 3
U 3`},
	{9, `R 2
D 2
L 2
U 2`},
	{8, `R 2
D 1
L 1
D 1
L 1
U 2`},
}

func TestPart1(t *testing.T) {
	lines := utils.ReadInput()
	is := BuildInstructions(lines)
	tr := is.Walk()
	part1Answer := tr.FilledArea()
	assert.Equal(t, 47675, part1Answer)
}

func TestPart1Shoelace(t *testing.T) {
	lines := utils.ReadInput()
	is := BuildInstructions(lines)
	part1Answer := ShoelaceTrapezoid(is)
	assert.Equal(t, 47675, part1Answer)
}
