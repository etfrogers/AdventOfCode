package main

import (
	"fmt"
	"utils"
	"utils/grid"
)

type Pattern struct {
	grid.Grid[string]
}
type Direction int

const (
	horz Direction = iota
	vert
)

type Reflection struct {
	direction   Direction
	indexBefore int
}

func (r *Reflection) Value() (value int) {
	switch r.direction {
	case vert:
		value = r.indexBefore
	case horz:
		value = r.indexBefore * 100
	}
	return
}

func sliceDifferences(s1, s2 []string) int {
	if len(s1) != len(s2) {
		panic("args to sliceDifferences must have the same lenth")
	}
	diffs := 0
	for i := range s1 {
		if s1[i] != s2[i] {
			diffs++
		}
	}
	return diffs
}

func (p *Pattern) ReflectsAbout(before int, direction Direction) (diff int) {
	var limit int
	switch direction {
	case horz:
		limit = p.NRows()
	case vert:
		limit = p.NCols()
	}
	diffs := 0
	for offset := 1; true; offset++ {
		left := before - (offset - 1)
		right := before + offset
		if left < 0 || right >= limit {
			break
		}
		var left_slice, right_slice []string
		switch direction {
		case horz:
			left_slice = p.GetRow(left)
			right_slice = p.GetRow(right)
		case vert:
			left_slice = p.GetCol(left)
			right_slice = p.GetCol(right)
		}
		diffs += sliceDifferences(left_slice, right_slice)
	}
	return diffs
}

func (p *Pattern) FindReflection(smudge bool) (reflection Reflection) {
	//search for horizontal reflections first
	diffTarget := 0
	if smudge {
		diffTarget = 1
	}
	for y := 0; y < p.NRows()-1; y++ {
		if p.ReflectsAbout(y, horz) == diffTarget {
			return Reflection{horz, y + 1}
		}
	}
	for x := 0; x < p.NCols()-1; x++ {

		if p.ReflectsAbout(x, vert) == diffTarget {
			return Reflection{vert, x + 1}
		}
	}
	return Reflection{}
}

func FindReflections(patterns []Pattern, smudge bool) []Reflection {
	refs := make([]Reflection, 0, len(patterns))
	for _, pattern := range patterns {
		r := pattern.FindReflection(smudge)
		refs = append(refs, r)
		// fmt.Println(i, r, len(refs))
	}
	return refs
}

func Summarize(patterns []Pattern, smudge bool) int {
	refs := FindReflections(patterns, smudge)
	return utils.Sum(utils.Map(refs, func(r Reflection) int { return r.Value() }))
}

func BuildPatterns(lines []string) []Pattern {
	arrs := utils.SplitSlice(lines, "")
	patterns := make([]Pattern, len(arrs))
	for i := range arrs {
		patterns[i] = Pattern{grid.NewFromStrings(arrs[i])}
	}
	return patterns
}

func main() {
	lines := utils.ReadInput()
	patterns := BuildPatterns(lines)
	part1Answer := Summarize(patterns, false)
	fmt.Printf("Day 13, Part 1 answer: %d\n", part1Answer)
	part2Answer := Summarize(patterns, true)
	fmt.Printf("Day 13, Part 2 answer: %d\n", part2Answer)
}
