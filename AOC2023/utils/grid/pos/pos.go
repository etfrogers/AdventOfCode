package pos

import (
	"utils/grid"
	dir "utils/grid/direction"
)

var moves = map[dir.Direction]Pos{
	dir.RIGHT: New(+1, 0),
	dir.LEFT:  New(-1, 0),
	dir.DOWN:  New(0, +1),
	dir.UP:    New(0, -1),
}

type Pos struct {
	x, y int
}

func New(x, y int) Pos { return Pos{x, y} }
func (p Pos) X() int   { return p.x }
func (p Pos) Y() int   { return p.y }

func (p *Pos) Add(other Pos) {
	// return Pos{p.x + other.x, p.y + other.y}
	p.x += other.x
	p.y += other.y
}

func (p *Pos) Move(dirn dir.Direction) {
	move := moves[dirn]
	p.Add(move)
}

func (p *Pos) Clone() Pos {
	return Pos{p.x, p.y}
}

func (p *Pos) DirectionFrom(to grid.Coord) (dirn dir.Direction) {
	dx := to.X() - p.X()
	dy := to.Y() - p.Y()
	switch {
	case dx == -1 && dy == 0:
		dirn = dir.LEFT
	case dx == 1 && dy == 0:
		dirn = dir.RIGHT
	case dx == 0 && dy == -1:
		dirn = dir.UP
	case dx == 0 && dy == 1:
		dirn = dir.DOWN
	default:
		panic("Unexpected case")
	}
	return
}

// --------------------

const Y_FACTOR int = 10_000_000

type XYNode struct {
	Pos
}

func NewNode(x, y int) XYNode {
	return XYNode{New(x, y)}
}

func (n XYNode) ID() (id int64) {
	return GenerateID(n.x, n.y)
}

func GenerateID(x, y int) (id int64) {
	return int64(y*Y_FACTOR + x)
}

func (n *XYNode) Clone() XYNode {
	return XYNode{n.Pos}
}
