package main

import (
	"strings"
	"testing"
	"utils"
	"utils/iter"

	"github.com/stretchr/testify/assert"
)

var testCase string = `.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....`

var energisedTiles = `######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..`

var testLines []string = strings.Split(testCase, "\n")

func TestNewEnergised(t *testing.T) {
	l := BuildLayout(testLines)
	str := l.EnergisedString()
	strIt := iter.FromString(str)
	mappedIt := iter.Map[string, bool](
		func(s string) bool { return s == "." || s == "\n" },
		strIt,
	)
	assert.True(t, iter.All(mappedIt))
}

func TestEnergised(t *testing.T) {
	l := BuildLayout(testLines)
	l.Illuminate(Beam{0, 0, RIGHT})
	assert.Equal(t, energisedTiles, l.EnergisedString())
}

func TestNEnergised(t *testing.T) {
	l := BuildLayout(testLines)
	l.Illuminate(Beam{0, 0, RIGHT})
	assert.Equal(t, 46, l.NEnergised())
}

func TestPart1(t *testing.T) {
	lines := utils.ReadInput()
	layout := BuildLayout(lines)
	layout.Illuminate(Beam{0, 0, RIGHT})
	part1Answer := layout.NEnergised()
	assert.Equal(t, 7482, part1Answer)
}

func TestMostEnergetic(t *testing.T) {
	l := BuildLayout(testLines)
	bs := l.MostEnergetic()
	expectedBeam := Beam{3, 0, DOWN}
	expectedScore := 51
	assert.Equal(t, expectedBeam, bs.beam)
	assert.Equal(t, expectedScore, bs.score)
}
