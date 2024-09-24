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

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/simple"
)

type Trails struct {
	grid.Grid[string]
	net                simple.DirectedGraph
	startNode, endNode graph.Node
}

type Path struct {
	visited *set.Set[grid.Coord]
	start   pos.Pos
	pos     pos.Pos
}

func (p *Path) Len() int {
	return p.visited.Len()
}

func (p *Path) Clone() Path {
	v := p.visited.Clone()
	return Path{&v, p.start.Clone(), p.pos.Clone()}
}

func NewTrails(lines []string) Trails {
	return Trails{grid.NewFromStrings(lines), *simple.NewDirectedGraph(), nil, nil}
}

var allDirs []direction.Direction = iter.ToSlice(direction.All())

func (t Trails) buildNet() {
	paths := stack.New[Path]()
	sn := pos.NewNode(1, 0)
	t.startNode = sn
	paths.Push(Path{pos: sn.Pos, visited: set.New[grid.Coord]()})
	walked := grid.Full(t.NCols(), t.NRows(), false)
	var newPaths []Path
	for paths.Len() > 0 {
		currPath, _ := paths.Pop()

		foundFork := false
		for !foundFork {
			if currPath.pos.Y() == t.NRows()-1 {
				t.endNode = pos.XYNode{Pos: currPath.pos}
				foundFork = true
			}

			walked.SetC(currPath.pos, true)

			var dirs []direction.Direction
			if ch := t.GetC(currPath.pos); ch == "." {
				dirs = allDirs
			} else {
				dirs = []direction.Direction{direction.FromArrowString(ch)}
			}
			validPaths := make([]Path, 0, len(dirs))
			for _, dir := range dirs {
				newPath := currPath.Clone()
				newPath.pos.Move(dir)
				if t.InsideC(newPath.pos) &&
					t.GetC(newPath.pos) != "#" &&
					!walked.GetC(newPath.pos) {

					validPaths = append(validPaths, newPath)
				}

			}
			nTrue := len(validPaths)
			if nTrue > 1 {
				foundFork = true
			} else {
				p := validPaths[0]
				currPath.pos = p.pos
			}
		}
		// have found a fork and it's stored in currPath
		edge := t.net.NewEdge()
		paths.PushAll(newPaths...)
	}
}

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
	t.buildNet()
	return slices.Max(t.PossiblePathLengths())
}

func main() {
	lines := utils.ReadInput()
	t := NewTrails(lines)
	part1Answer := t.LongestPath()
	fmt.Printf("Day 23, Part 1 answer: %d\n", part1Answer)
}
