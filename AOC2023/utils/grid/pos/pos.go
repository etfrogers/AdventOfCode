package pos

import dir "utils/grid/direction"

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
