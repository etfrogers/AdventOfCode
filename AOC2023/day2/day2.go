package main

import (
	"day2/game"
	"fmt"
	"os"
	"strings"
	"utils"
)

func Checksum(lines []string, bag game.Bag) int {
	games := game.GameSliceFromLines(lines)
	checksum := 0
	for _, game := range games {
		if game.IsValid(bag) {
			checksum += game.ID
		}
	}
	return checksum
}

func PowerChecksum(lines []string) int {
	games := game.GameSliceFromLines(lines)
	checksum := 0
	for _, game := range games {
		checksum += game.MinBagPower()
	}
	return checksum
}

func main() {
	doc, err := os.ReadFile("input.txt")
	utils.Check(err)
	lines := strings.Split(string(doc), "\n")
	bag := game.Bag{game.Red: 12, game.Green: 13, game.Blue: 14}

	checksum := Checksum(lines, bag)
	fmt.Printf("Day 2, Part 1 Answer: %d\n", checksum)

	powerChecksum := PowerChecksum(lines)
	fmt.Printf("Day 2, Part 2 Answer: %d\n", powerChecksum)

}
