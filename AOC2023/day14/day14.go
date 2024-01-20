package main

import (
	"fmt"
	"utils"
	"utils/counter"
	"utils/grid"
)

type Rocks struct {
	grid.Grid[Rock]
}

type Rock int

const (
	EMPTY Rock = iota
	ROUND
	CUBE
)

type Dir int

const (
	NORTH Dir = iota
	SOUTH
	EAST
	WEST
)

var ROCK_MAP map[Rock]string = map[Rock]string{
	EMPTY: ".",
	ROUND: "O",
	CUBE:  "#",
}

var ROCK_INV_MAP = invertMap(ROCK_MAP)

func invertMap[T, V comparable](m map[T]V) map[V]T {
	r := make(map[V]T)
	for k, v := range m {
		r[v] = k
	}
	return r
}

func StringToRock(s string) Rock {
	r, ok := ROCK_INV_MAP[s]
	if !ok {
		panic("unexpected value")
	}
	return r
}

func RockToString(r Rock) string {
	s, ok := ROCK_MAP[r]
	if !ok {
		panic("unexpected value")
	}
	return s
}

func NewRocks(lines []string) Rocks {
	temp := grid.NewFromStrings(lines)
	return Rocks{grid.Map(&temp, StringToRock)}
}

func (r *Rocks) String() string {
	temp := grid.Map(&(r.Grid), RockToString)
	return temp.String()
}

func (r *Rocks) Tilt(d Dir) {
	var invert, colMajor bool
	switch d {
	case NORTH:
		invert, colMajor = false, false
	case SOUTH:
		invert, colMajor = true, false
	case WEST:
		invert, colMajor = false, true
	case EAST:
		invert, colMajor = true, true
	default:
		panic("not implemented")
	}
	it := r.IndIterator(invert, colMajor)
	for x, y, ok := it.Next(); ok; x, y, ok = it.Next() {
		r.moveRockAt(x, y, d)
	}
}

func (r *Rocks) moveRockAt(x, y int, d Dir) {
	switch d {
	case NORTH:
		y_ := y
		for y_ > 0 && r.Get(x, y_) == ROUND && r.Get(x, y_-1) == EMPTY {
			r.Set(x, y_, EMPTY)
			r.Set(x, y_-1, ROUND)
			y_--
		}
	case SOUTH:
		y_ := y
		for y_ < r.NRows()-1 && r.Get(x, y_) == ROUND && r.Get(x, y_+1) == EMPTY {
			r.Set(x, y_, EMPTY)
			r.Set(x, y_+1, ROUND)
			y_++
		}
	case WEST:
		x_ := x
		for x_ > 0 && r.Get(x_, y) == ROUND && r.Get(x_-1, y) == EMPTY {
			r.Set(x_, y, EMPTY)
			r.Set(x_-1, y, ROUND)
			x_--
		}
	case EAST:
		x_ := x
		for x_ < r.NCols()-1 && r.Get(x_, y) == ROUND && r.Get(x_+1, y) == EMPTY {
			r.Set(x_, y, EMPTY)
			r.Set(x_+1, y, ROUND)
			x_++
		}
	default:
		panic("not implemented")
	}
}

func (r *Rocks) TotalLoading() int {
	score := 0
	for y := 0; y < r.NCols(); y++ {
		rowScore := r.NRows() - y
		c := counter.New(r.GetRow(y)...)
		nRocks := c.Get(ROUND)
		score += rowScore * nRocks
	}
	return score
}

func (r *Rocks) Cycle() {
	r.Tilt(NORTH)
	r.Tilt(WEST)
	r.Tilt(SOUTH)
	r.Tilt(EAST)
}

func main() {
	lines := utils.ReadInput()
	rocks := NewRocks(lines)
	rocks.Tilt(NORTH)
	part1Answer := rocks.TotalLoading()
	fmt.Printf("Day 14, Part 1 answer: %d\n", part1Answer)
}
