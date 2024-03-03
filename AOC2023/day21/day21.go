package main

import (
	"fmt"
	"utils"
	"utils/grid"
	"utils/grid/direction"
	"utils/grid/pos"
	"utils/set"
)

type Garden struct {
	grid.Grid[string]
	start pos.Pos
}

func NewGarden(lines []string) Garden {
	g := grid.NewFromStrings(lines)
	startx, starty := g.Find("S")
	return Garden{g, pos.New(startx, starty)}
}

func (g *Garden) FindStepOutcomes(n int) int {
	paths := set.New[pos.Pos]()
	paths.Add(g.start)
	for range n {
		newPaths := set.New[pos.Pos]()
		for path := range paths.All() {
			for dir := range direction.All() {
				newPath := path.Clone()
				newPath.Move(dir)

				if g.InsideC(newPath) && g.GetC(newPath) != "#" {
					newPaths.Add(newPath)
				}
			}
		}
		paths = newPaths
	}
	nPaths := paths.Len()
	// g.Render(paths)
	return nPaths
}

func (g *Garden) Render(ps *set.Set[pos.Pos]) {
	mapWithPath := g.Clone()
	for s := range ps.All() {
		mapWithPath.Set(s.X(), s.Y(), "O")
	}
	fmt.Println(mapWithPath.String())
}

func main() {
	lines := utils.ReadInput()
	g := NewGarden(lines)
	part1Answer := g.FindStepOutcomes(64)
	fmt.Printf("Day 21, Part 1 answer: %d\n", part1Answer)
}
