package main

import (
	"fmt"
	"utils"
	"utils/grid"
	"utils/set"
)

type Pos struct {
	x, y int
}

func (p Pos) X() int { return p.x }
func (p Pos) Y() int { return p.y }

func (p Pos) Add(other Pos) Pos {
	return Pos{p.x + other.x, p.y + other.y}
}

type Garden struct {
	grid.Grid[string]
	start Pos
}

func NewGarden(lines []string) Garden {
	g := grid.NewFromStrings(lines)
	startx, starty := g.Find("S")
	return Garden{g, Pos{startx, starty}}
}

var STEPS = []Pos{{+1, 0}, {-1, 0}, {0, +1}, {0, -1}}

func (g *Garden) FindStepOutcomes(n int) int {
	paths := set.New[Pos]()
	paths.Add(g.start)
	for range n {
		newPaths := set.New[Pos]()
		for path := range paths.All() {
			for _, step := range STEPS {
				newPath := path.Add(step)

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

func (g *Garden) Render(ps *set.Set[Pos]) {
	mapWithPath := g.Clone()
	for s := range ps.All() {
		mapWithPath.Set(s.x, s.y, "O")
	}
	fmt.Println(mapWithPath.String())
}

func main() {
	lines := utils.ReadInput()
	g := NewGarden(lines)
	part1Answer := g.FindStepOutcomes(64)
	fmt.Printf("Day 21, Part 1 answer: %d\n", part1Answer)
}
