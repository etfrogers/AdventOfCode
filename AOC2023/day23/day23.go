package main

import (
	"fmt"
	"slices"
	"utils"
	"utils/grid"
	"utils/grid/direction"
	"utils/grid/pos"
	"utils/iter"
	"utils/set"
	"utils/stack"
)

type Trails struct {
	grid.Grid[string]
}

type Path struct {
	visited *set.Set[grid.Coord]
	pos     pos.Pos
}

func (p *Path) Len() int {
	return p.visited.Len()
}

func (p *Path) Clone() Path {
	v := p.visited.Clone()
	return Path{&v, p.pos.Clone()}
}

func NewTrails(lines []string) Trails {
	return Trails{grid.NewFromStrings(lines)}
}

var allDirs []direction.Direction = iter.ToSlice(direction.All())

func (t Trails) AllPaths() []Path {
	outputs := make([]Path, 0)
	paths := stack.New[Path]()
	paths.Push(Path{pos: pos.New(1, 0), visited: set.New[grid.Coord]()})
	for paths.Len() > 0 {
		currPath, _ := paths.Pop()

		if currPath.pos.Y() == t.NRows()-1 {
			outputs = append(outputs, currPath)
			continue
		}

		currPath.visited.Add(currPath.pos)
		var dirs []direction.Direction
		if ch := t.GetC(currPath.pos); ch == "." {
			dirs = allDirs
		} else {
			dirs = []direction.Direction{direction.FromArrowString(ch)}
		}
		for _, dir := range dirs {
			newPath := currPath.Clone()
			newPath.pos.Move(dir)
			if t.InsideC(newPath.pos) &&
				t.GetC(newPath.pos) != "#" &&
				!newPath.visited.Contains(newPath.pos) {
				paths.Push(newPath)
			}
		}
	}
	return outputs
}

func (t Trails) PossiblePathLengths() []int {
	ps := t.AllPaths()
	return utils.Map(ps, func(p Path) int { return p.Len() })
}

func (t Trails) LongestPath() int {
	return slices.Max(t.PossiblePathLengths())
}

func main() {
	lines := utils.ReadInput()
	t := NewTrails(lines)
	part1Answer := t.LongestPath()
	fmt.Printf("Day 23, Part 1 answer: %d\n", part1Answer)
}
