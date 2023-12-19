package main

import (
	"day2/game"
	"os"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

var testData = `Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green`

var testBag game.Phase = game.Phase{game.Red: 12, game.Green: 13, game.Blue: 14}

var testLines []string

func init() {
	testLines = strings.Split(testData, "\n")
}

func TestGameConstruction(t *testing.T) {
	testCases := []struct {
		n_phases int
		events   game.Phase
	}{
		{3, game.Phase{game.Blue: 3, game.Red: 4}},
		{3, nil},
		{3, nil},
		{3, nil},
		{2, nil},
	}
	for tc_i, tc := range testCases {
		t.Run(string(testLines[tc_i]), func(t *testing.T) {
			game_ := game.GameFromLine(testLines[tc_i])
			assert.Equal(t, game_.ID, tc_i+1)
			assert.Equal(t, game_.NPhases(), tc.n_phases)
			if tc.events != nil {
				assert.Equal(t, tc.events, game_.Phases[0])
			}
		})
	}
}

func TestGameValidity(t *testing.T) {
	testCases := []bool{true, true, false, false, true}
	for tc_i, tc := range testCases {
		t.Run(string(testLines[tc_i]), func(t *testing.T) {
			game_ := game.GameFromLine(testLines[tc_i])
			assert.Equal(t, game_.IsValid(testBag), tc)
		})
	}
}

func TestPart1(t *testing.T) {
	doc, err := os.ReadFile("input.txt")
	game.Check(err)
	lines := strings.Split(string(doc), "\n")
	bag := game.Phase{game.Red: 12, game.Green: 13, game.Blue: 14}

	checksum := Checksum(lines, bag)
	assert.Equal(t, checksum, 2207)
}
