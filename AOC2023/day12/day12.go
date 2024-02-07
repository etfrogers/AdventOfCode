package main

import (
	"fmt"
	"slices"
	"strings"
	"utils"
	"utils/stack"
	"utils/tree"
)

type Record struct {
	Listing []rune
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

func (r *Record) buildTree() *tree.Tree[rune] {
	root := tree.NewNode[rune](NULL)
	t := tree.New[rune](root)
	leaves := stack.New[*tree.Node[rune]]()
	leaves.Push(root)
	for i, s := range r.Listing {
		newLeaves := stack.New[*tree.Node[rune]]()
		for leaf, ok := leaves.Pop(); ok; leaf, ok = leaves.Pop() {
			currentPath := pathFromNode(t, leaf)
			var chars []rune
			if s == '?' {
				chars = []rune{'#', '.'}
			} else {
				chars = []rune{s}
			}
			leafIsValid := false
			for _, testChar := range chars {
				testPath := append(currentPath, testChar)
				testGroups := calculateGroups(testPath)
				lastGroup := len(testGroups)
				if testChar == '#' && i < len(r.Listing)-1 {
					// the last group could still increase if more #'s come up,
					// so don't count it as a miss if the last char doesn't match
					lastGroup--
				}
				if i == len(r.Listing)-1 {
					lastGroup = len(r.Groups)
				}
				if (len(testGroups) <= len(r.Groups)) && slices.Equal(r.Groups[:lastGroup], testGroups[:lastGroup]) {
					n := tree.NewNode(testChar)
					leaf.AddChild(n)
					newLeaves.Push(n)
					leafIsValid = true
				}
			}
			if !leafIsValid {
				t.PruneBranchTo(leaf)
			}
		}
		leaves = newLeaves
	}
	return t
}

func pathFromNode(t *tree.Tree[rune], n *tree.Node[rune]) []rune {
	vals := t.NodeToRootValues(n)
	slices.Reverse(vals)
	vals = vals[1:] // drop root value - NULL char
	return vals
}

func (r *Record) PossibleConfigs() [][]rune {
	t := r.buildTree()
	// t.Render()
	leaves := t.GetLeaves()
	paths := utils.Map(leaves, func(n *tree.Node[rune]) []rune { return pathFromNode(t, n) })
	// paths = utils.Filter(paths, func(listing []rune) bool { return slices.Equal(calculateGroups(listing), r.Groups) })
	return paths
}

func NewRecordSet(lines []string, unfold bool) RecordSet {
	return utils.Map(lines, func(s string) Record { return NewRecord(s, unfold) })
}

func (rs *RecordSet) TotalConfigs() int {
	return utils.Sum(utils.Map(*rs, func(r Record) int { return len(r.PossibleConfigs()) }))
}

func main() {
	lines := utils.ReadInput()
	rs := NewRecordSet(lines, false)
	part1Answer := rs.TotalConfigs()
	fmt.Printf("Day 12, Part 1 answer: %d\n", part1Answer)
}
