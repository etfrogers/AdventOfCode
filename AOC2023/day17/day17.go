package main

import (
	"fmt"
	"slices"
	"utils"
	"utils/grid"
	"utils/heap"
)

type CityMap struct {
	grid.Grid[int]
}

type Direction int

const (
	NORTH Direction = iota
	EAST
	SOUTH
	WEST
)

type visitKey struct {
	x, y  int
	dir   Direction
	steps int
}

type Path struct {
	totalLoss  int
	x, y       int
	dir        Direction
	stepsInDir int
	history    []visitKey
	ultra      bool
}

func (d Direction) String() (s string) {
	switch d {
	case NORTH:
		s = "^"
	case SOUTH:
		s = "v"
	case EAST:
		s = ">"
	case WEST:
		s = "<"
	}
	return s
}

func (p Path) Less(other heap.Heaper) bool {
	return p.totalLoss < other.(Path).totalLoss
}

func (p Path) PossibleDirs() []Direction {
	left := p.dir - 1
	if left < 0 {
		left = WEST
	}
	right := (p.dir + 1) % 4
	var dirs []Direction
	if p.ultra {
		switch {
		case p.stepsInDir < 4:
			dirs = []Direction{p.dir}
		case p.stepsInDir >= 4 && p.stepsInDir < 10:
			dirs = []Direction{left, right, p.dir}
		case p.stepsInDir >= 10:
			dirs = []Direction{left, right}
		}
	} else {
		dirs = []Direction{left, right}
		if p.stepsInDir < 3 {
			dirs = append(dirs, p.dir)
		}
	}
	return dirs
}

func (p Path) CanStop() bool {
	return !p.ultra || p.stepsInDir >= 4
}

func (p Path) VisitKey() visitKey {
	return visitKey{x: p.x, y: p.y, dir: p.dir, steps: p.stepsInDir}
}

func (p Path) Clone() Path {
	return Path{
		totalLoss:  p.totalLoss,
		x:          p.x,
		y:          p.y,
		dir:        p.dir,
		stepsInDir: p.stepsInDir,
		ultra:      p.ultra,
		history:    slices.Clone(p.history),
	}
}

func (p *Path) Move(m CityMap, dir Direction) (valid bool) {
	p.history = append(p.history, p.VisitKey())
	switch dir {
	case NORTH:
		p.y--
		if p.y < 0 {
			return false
		}
	case SOUTH:
		p.y++
		if p.y >= m.NRows() {
			return false
		}
	case EAST:
		p.x++
		if p.x >= m.NCols() {
			return false
		}
	case WEST:
		p.x--
		if p.x < 0 {
			return false
		}
	}
	if dir == p.dir {
		p.stepsInDir++
	} else {
		p.stepsInDir = 1
	}
	p.dir = dir
	p.totalLoss += m.Get(p.x, p.y)
	return true
}

func NewMap(lines []string) CityMap {
	g := grid.NewFromStrings(lines)
	return CityMap{grid.Map(&g, utils.AtoiError)}
}

func (m CityMap) leastLoss(ultra bool) int {
	paths := heap.NewSliceHeap[Path]()
	visited := make(map[visitKey]int, m.NElem()*4*3)
	paths.PushH(Path{x: 0, y: 0, dir: EAST, totalLoss: 0, stepsInDir: 0, ultra: ultra, history: []visitKey{}})
	for {
		path := paths.PopH()
		for _, dir := range path.PossibleDirs() {
			newPath := path.Clone()
			if newPath.Move(m, dir) {
				key := newPath.VisitKey()
				if prevLoss, ok := visited[key]; ok {
					if prevLoss > newPath.totalLoss {
						panic("unexpected state")
					}
				} else {
					visited[key] = newPath.totalLoss
					paths.PushH(newPath)
				}
				if newPath.CanStop() && newPath.x == m.NCols()-1 && newPath.y == m.NRows()-1 {
					// m.Render(newPath)
					return newPath.totalLoss
				}
			}
		}
	}
}

func (m *CityMap) Render(p Path) {
	mapWithPath := grid.Map(&(m.Grid), func(s int) string { return fmt.Sprint(s) })
	for _, s := range p.history {
		symbol := s.dir.String()
		mapWithPath.Set(s.x, s.y, symbol)
	}
	fmt.Println(mapWithPath.String())
}

func main() {
	lines := utils.ReadInput()
	m := NewMap(lines)
	part1Answer := m.leastLoss(false)
	fmt.Printf("Day 17, Part 1 answer: %d\n", part1Answer)
	part2Answer := m.leastLoss(true)
	fmt.Printf("Day 17, Part 1 answer: %d\n", part2Answer)
}
