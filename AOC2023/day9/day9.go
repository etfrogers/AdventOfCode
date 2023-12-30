package main

import (
	"fmt"
	"strings"
	"utils"
)

type Sequence []int

type SequenceList []Sequence

func NewSequence(line string) Sequence {
	strs := strings.Split(line, " ")
	ints := utils.Map(strs, utils.AtoiError)
	return Sequence(ints)
}

func NewSequenceList(lines []string) SequenceList {
	return utils.Map(lines, NewSequence)
}

func allZeros(s []int) bool {
	return utils.All(utils.Map(s, func(x int) bool { return x == 0 }))
}

func diff(input []int) []int {
	d := make([]int, len(input)-1)
	for i := 0; i < len(input)-1; i++ {
		d[i] = input[i+1] - input[i]
	}
	return d
}

func lastElem[T any](s []T) T {
	return s[len(s)-1]
}

func (s *Sequence) Extrapolate() int {
	diffs := [][]int{}
	diffs = append(diffs, *s)
	for !allZeros(diffs[len(diffs)-1]) {
		diffs = append(diffs, diff(lastElem(diffs)))
	}

	for i := len(diffs) - 1; i >= 0; i-- {
		var newVal int
		if i == len(diffs)-1 {
			newVal = 0
		} else {
			newVal = lastElem(diffs[i+1]) + lastElem(diffs[i])
		}
		diffs[i] = append(diffs[i], newVal)
	}
	return lastElem(diffs[0])
}

func (sl *SequenceList) SumExtrapolate() int {
	return utils.Sum(utils.Map[Sequence, int](*sl, func(s Sequence) int { return s.Extrapolate() }))
}

func main() {
	lines := utils.ReadInput()
	sequences := NewSequenceList(lines)
	part1Answer := sequences.SumExtrapolate()
	fmt.Printf("Day 9, Part 1 answer: %d\n", part1Answer)
}
