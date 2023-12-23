package main

import (
	"fmt"
	"utils"
)

func main() {
	lines := utils.ReadInput()
	cards := NewCardSlice(lines)
	part1Answer := TotalScore(cards)
	fmt.Printf("Day 4, Part 1 answer: %d\n", part1Answer)
	part2Answer, _ := ProcessCopies(cards)
	fmt.Printf("Day 4, Part 1 answer: %d\n", part2Answer)
}
