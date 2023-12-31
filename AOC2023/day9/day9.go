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

func (s *Sequence) Extrapolate() (int, int) {
	diffs := [][]int{}
	diffs = append(diffs, *s)
	for !allZeros(diffs[len(diffs)-1]) {
		diffs = append(diffs, diff(lastElem(diffs)))
	}

	startVal, endVal := 0, 0
	for i := len(diffs) - 2; i >= 0; i-- {
		endVal += lastElem(diffs[i])
		startVal = diffs[i][0] - startVal
	}
	return startVal, endVal
}

func (sl *SequenceList) SumExtrapolate() (startSum, endSum int) {
	startSum, endSum = 0, 0
	for _, s := range *sl {
		startVal, endVal := s.Extrapolate()
		startSum += startVal
		endSum += endVal
	}
	return
}

func main() {
	lines := utils.ReadInput()
	sequences := NewSequenceList(lines)
	part2Answer, part1Answer := sequences.SumExtrapolate()
	fmt.Printf("Day 9, Part 1 answer: %d\n", part1Answer)
	fmt.Printf("Day 9, Part 2 answer: %d\n", part2Answer)
}
