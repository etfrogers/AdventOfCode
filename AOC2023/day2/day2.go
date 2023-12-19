package main

import (
	"day2/game"
	"fmt"
	"os"
	"strings"
)

func Checksum(lines []string, bag game.Phase) int {
	games := game.GameSliceFromLines(lines)
	// filtered := []game.Game{}
	checksum := 0
	for _, game := range games {
		if game.IsValid(bag) {
			// filtered = append(filtered, game)
			checksum += game.ID
		}
	}
	return checksum
}

func main() {
	doc, err := os.ReadFile("input.txt")
	game.Check(err)
	lines := strings.Split(string(doc), "\n")
	bag := game.Phase{game.Red: 12, game.Green: 13, game.Blue: 14}

	checksum := Checksum(lines, bag)
	fmt.Printf("Day 2, Part 1 Answer: %d\n", checksum)

}
