package main

import (
	"fmt"
	"strings"
	"utils"
)

func Hash(s string) int {
	hash := 0
	for _, r := range []rune(s) {
		hash += int(r)
		hash *= 17
		hash %= 256
	}
	return hash
}

func HashSlice(csv string) []int {
	tokens := strings.Split(csv, ",")
	return utils.Map(tokens, Hash)
}

func Checksum(csv string) int {
	return utils.Sum(HashSlice(csv))
}

func main() {
	input := utils.ReadInput()[0]
	part1Answer := Checksum(input)
	fmt.Printf("Day 15, Part 1 answer: %d\n", part1Answer)
}
