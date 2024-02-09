package main

import (
	"fmt"
	"slices"
	"strings"
	"utils"
	"utils/stack"
)

type Path []rune

type Record struct {
	Listing Path
	Groups  []int
}

type RecordSet []Record

const N_UNFOLD = 5

func NewRecord(s string, unfold bool) Record {
	listing, groupStr, ok := strings.Cut(s, " ")
	if !ok {
		panic("failed to parse")
	}
	tokens := strings.Split(groupStr, ",")
	groups := utils.Map(tokens, utils.AtoiError)
	if unfold {
		origGroups := slices.Clone(groups)
		origListing := listing
		for i := 1; i < N_UNFOLD; i++ {
			listing = listing + "?" + origListing
			groups = append(groups, origGroups...)
		}
	}
	return Record{Listing: []rune(listing), Groups: groups}
}

func (r *Record) CalculateGroups() (groups []int) {
	return calculateGroups(r.Listing)
}

func calculateGroups(listing []rune) (groups []int) {
	groups = make([]int, 0, 10)
	inGroup := false
	currentGroup := 0
	for _, spring := range listing {
		switch {
		case !inGroup && spring == '#':
			currentGroup++
			inGroup = true
		case inGroup && spring == '#':
			currentGroup++
		case inGroup && spring == '.':
			groups = append(groups, currentGroup)
			currentGroup = 0
			inGroup = false
		case !inGroup && spring == '.':
			// do nothing
		case spring == '?':
			return
		default:
			panic("unexpected value")
		}
	}
	if currentGroup > 0 {
		groups = append(groups, currentGroup)
	}
	return
}

const NULL = rune(0)

func (r *Record) NPossibleConfigs() int {
	nPaths := 0
	workingPaths := stack.New[Path]()
	workingPaths.Push(Path{})

	for workingPaths.Len() > 0 {
		currentPath, _ := workingPaths.Pop()
		i := len(currentPath)
		s := r.Listing[i]
		var chars []rune
		if s == '?' {
			chars = []rune{'#', '.'}
		} else {
			chars = []rune{s}
		}
		for _, testChar := range chars {
			newPath := append(currentPath, testChar)
			testGroups := calculateGroups(newPath)
			lastGroup := len(testGroups)
			gLen := len(r.Groups)
			// label := fmt.Sprintf("%s - %v", string(newPath), testGroups)
			if lastGroup > gLen {
				// if we already have too many groups, this path is bad.
				// fmt.Println("- " + label)
				continue

			}
			if testChar == '#' && i < len(r.Listing)-1 && testGroups[lastGroup-1] <= r.Groups[lastGroup-1] {
				// the last group could still increase if more #'s come up,
				// so don't count it as a miss if the last char doesn't match
				// unless the last group is already too large
				lastGroup--
			}
			if i == len(r.Listing)-1 {
				lastGroup = gLen
			}
			tgLen := len(testGroups)
			if (tgLen <= gLen) && lastGroup <= tgLen && lastGroup <= gLen && slices.Equal(r.Groups[:lastGroup], testGroups[:lastGroup]) {
				if len(newPath) == len(r.Listing) {
					nPaths++
					// fmt.Println("O " + label)
				} else {
					workingPaths.Push(slices.Clone(newPath))
					// fmt.Println("+ " + label)
				}
				// } else {
				// fmt.Println("- " + label)
			}
		}
	}
	// fmt.Println("------------------")
	return nPaths
}

func NewRecordSet(lines []string, unfold bool) RecordSet {
	return utils.Map(lines, func(s string) Record { return NewRecord(s, unfold) })
}

func (rs *RecordSet) TotalConfigs() int {
	tasks := stack.New[Record]()
	nTasks := len(*rs)
	nProc := 12
	tasks.PushAll(*rs...)
	c := make(chan int, nProc*2)

	for i := 0; i < nProc; i++ {
		fmt.Printf("starting worker %d\n", i)
		go func() {
			for {
				fmt.Printf("%d / %d\n", nTasks-tasks.Len(), nTasks)
				if r, ok := tasks.Pop(); ok {
					c <- r.NPossibleConfigs()
				} else {
					break
				}
			}
		}()
	}

	results := make([]int, nTasks)
	for j := 0; j < nTasks; j++ {
		results[j] = <-c
	}
	return utils.Sum(results)
}

func main() {
	lines := utils.ReadInput()
	rs := NewRecordSet(lines, false)
	part1Answer := rs.TotalConfigs()
	fmt.Printf("Day 12, Part 1 answer: %d\n", part1Answer)

	rs2 := NewRecordSet(lines, true)
	part2Answer := rs2.TotalConfigs()
	fmt.Printf("Day 12, Part 2 answer: %d\n", part2Answer)

}
