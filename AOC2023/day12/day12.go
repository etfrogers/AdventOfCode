package main

import (
	"fmt"
	"slices"
	"strings"
	"utils"
	"utils/heap"
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

type Cursor struct {
	Position        int
	RemainingGroups []int
	InGroup         bool
	Record          *Record
	PathsToHere     int
}

func (c1 *Cursor) Equal(c2 Cursor) bool {
	if c1.Position != c2.Position {
		return false
	}
	return slices.Equal(c1.RemainingGroups, c2.RemainingGroups)
}

func (c Cursor) Clone() Cursor {
	return Cursor{
		Position:        c.Position,
		RemainingGroups: slices.Clone(c.RemainingGroups),
		InGroup:         c.InGroup,
		Record:          c.Record,
		PathsToHere:     c.PathsToHere,
	}
}

func (c *Cursor) processHash() (validStep bool) {
	if len(c.RemainingGroups) == 0 {
		// if there are no more groups, a # is not a valid option
		return false
	}
	c.RemainingGroups[0]--
	c.InGroup = true
	return c.RemainingGroups[0] >= 0
}

func (c *Cursor) processDot() (validStep bool) {
	if c.InGroup {
		if c.RemainingGroups[0] != 0 {
			return false
		}
		c.RemainingGroups = c.RemainingGroups[1:]
		c.InGroup = false
	}
	// if not in group, do nothing
	return true
}

func (c *Cursor) Advance() (newCursors []Cursor) {
	retVal := func(b bool) []Cursor {
		if b {
			return []Cursor{*c}
		} else {
			return []Cursor{}
		}
	}
	c.Position++
	spring := c.Record.Listing[c.Position]
	switch spring {
	case '#':
		newCursors = retVal(c.processHash())

	case '.':
		newCursors = retVal(c.processDot())
	case '?':
		newCursors = make([]Cursor, 0, 2)
		c2 := c.Clone()
		if c.processHash() {
			newCursors = append(newCursors, *c)
		}
		if c2.processDot() {
			newCursors = append(newCursors, c2)
		}
	default:
		panic("unexpected value")
	}
	return
}

const NULL = rune(0)

func (r *Record) NPossibleConfigs() int {
	nPaths := 0
	cursors := heap.NewSliceHeap[Cursor]()
	baseCursor := Cursor{Position: -1, RemainingGroups: slices.Clone(r.Groups), Record: r, PathsToHere: 1}
	cursors.Push(baseCursor)

	for cursors.Len() > 0 {
		cursor := cursors.PopH()
		for cursors.Len() > 0 && cursors.Peek().Equal(cursor) {
			equiv := cursors.PopH()
			cursor.PathsToHere += equiv.PathsToHere
		}
		if cursor.Position == len(r.Listing)-1 {
			if len(cursor.RemainingGroups) == 0 || (len(cursor.RemainingGroups) == 1 && cursor.RemainingGroups[0] == 0) {
				nPaths += cursor.PathsToHere
			}
			continue
		}
		newCursors := cursor.Advance()
		cursors.PushH(newCursors...)
	}
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

	for i := range nProc {
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
