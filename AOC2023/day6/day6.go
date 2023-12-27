package main

import (
	"fmt"
	"strings"
	"utils"
)

type Race struct {
	time           int
	recordDistance int
}

type Result struct {
	holdTime         int
	achievedDistance int
}

func (r *Race) PossibleResults() []Result {
	results := make([]Result, r.time+1)
	for holdTime := 0; holdTime <= r.time; holdTime++ {
		speed := holdTime
		moveTime := r.time - holdTime
		moveDist := speed * moveTime
		results[holdTime] = Result{holdTime, moveDist}
	}
	return results
}

func (r *Race) NWinners() int {
	results := r.PossibleResults()
	n := 0
	for _, result := range results {
		if result.achievedDistance > r.recordDistance {
			n++
		}
	}
	return n
}

func parseLine(line string) []int {
	_, dataStr, _ := strings.Cut(line, ":")
	dataSlice := utils.DropEmpty(strings.Split(dataStr, " "))
	return utils.Map[string, int](dataSlice, utils.AtoiError)
}

func NewRaces(lines []string) []Race {
	timeStr := lines[0]
	distStr := lines[1]
	times := parseLine(timeStr)
	dists := parseLine(distStr)

	races := make([]Race, len(times))
	for i, time := range times {
		races[i] = Race{time, dists[i]}
	}
	return races
}

func main() {
	lines := utils.ReadInput()
	races := NewRaces(lines)
	nWinners := utils.Map(races, func(x Race) int { return x.NWinners() })
	part1Answer := utils.Prod(nWinners)
	fmt.Printf("Day 6, Part 1 answer: %d\n", part1Answer)
}
