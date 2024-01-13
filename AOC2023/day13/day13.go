package main

import (
	"fmt"
	"slices"
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

func (p *Pattern) ReflectsAbout(before int, direction Direction) bool {
	var limit int
	switch direction {
	case horz:
		limit = p.NRows()
	case vert:
		limit = p.NCols()
	}
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
		if !slices.Equal(left_slice, right_slice) {
			return false
		}
	}
	return true
}

func (p *Pattern) FindReflection() (reflection Reflection) {
	//search for horizontal reflections first
	for y := 0; y < p.NRows()-1; y++ {
		if p.ReflectsAbout(y, horz) {
			reflection = Reflection{horz, y + 1}
		}
	}
	for x := 0; x < p.NCols()-1; x++ {
		if p.ReflectsAbout(x, vert) {
			reflection = Reflection{vert, x + 1}
		}
	}
	return reflection
}

func FindReflections(patterns []Pattern) []Reflection {
	refs := make([]Reflection, 0, len(patterns))
	for i, pattern := range patterns {
		r := pattern.FindReflection()
		refs = append(refs, r)
		fmt.Println(i, r, len(refs))
	}
	return refs
}

func Summarize(patterns []Pattern) int {
	refs := FindReflections(patterns)
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
	part1Answer := Summarize(patterns)
	fmt.Printf("Day 13, Part 1 answer: %d\n", part1Answer)
}
