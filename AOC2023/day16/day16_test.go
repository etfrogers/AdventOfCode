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
	strIt := iter.FromStr(str)
	mappedIt := iter.Map[string, bool](
		func(s string) bool { return s == "." || s == "\n" },
		strIt,
	)
	assert.True(t, iter.All(mappedIt))
}

func TestEnergised(t *testing.T) {
	l := BuildLayout(testLines)
	l.Illuminate()
	assert.Equal(t, energisedTiles, l.EnergisedString())
}

func TestNEnergised(t *testing.T) {
	l := BuildLayout(testLines)
	l.Illuminate()
	assert.Equal(t, 46, l.NEnergised())
}

func TestPart1(t *testing.T) {
	lines := utils.ReadInput()
	layout := BuildLayout(lines)
	layout.Illuminate()
	part1Answer := layout.NEnergised()
	assert.Equal(t, 7482, part1Answer)
}
