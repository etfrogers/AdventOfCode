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

func NewRecord(s string) Record {
	listing, groupStr, ok := strings.Cut(s, " ")
	if !ok {
		panic("failed to parse")
	}
	tokens := strings.Split(groupStr, ",")
	groups := utils.Map(tokens, utils.AtoiError)
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
	for _, s := range r.Listing {
		newLeaves := stack.New[*tree.Node[rune]]()
		for leaf, ok := leaves.Pop(); ok; leaf, ok = leaves.Pop() {
			switch s {
			case '?':
				n := tree.NewNode('#')
				leaf.AddChild(n)
				newLeaves.Push(n)
				n = tree.NewNode('.')
				leaf.AddChild(n)
				newLeaves.Push(n)
			case '.', '#':
				n := tree.NewNode(s)
				leaf.AddChild(n)
				newLeaves.Push(n)
			default:
				panic("unexpected value")
			}
		}
		leaves = newLeaves
	}
	return t
}

func (r *Record) PossibleConfigs() [][]rune {
	t := r.buildTree()
	leaves := t.GetLeaves()
	paths := utils.Map(leaves, func(n *tree.Node[rune]) []rune {
		vals := t.NodeToRootValues(n)
		slices.Reverse(vals)
		vals = vals[1:] // drop root value - NULL char
		return vals
	})
	paths = utils.Filter(paths, func(listing []rune) bool { return slices.Equal(calculateGroups(listing), r.Groups) })
	return paths
}

func NewRecordSet(lines []string) RecordSet {
	return utils.Map(lines, NewRecord)
}

func (rs *RecordSet) TotalConfigs() int {
	return utils.Sum(utils.Map(*rs, func(r Record) int { return len(r.PossibleConfigs()) }))
}

func main() {
	lines := utils.ReadInput()
	rs := NewRecordSet(lines)
	part1Answer := rs.TotalConfigs()
	fmt.Printf("Day 12, Part 1 answer: %d\n", part1Answer)
}
