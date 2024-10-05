// use std::collections::HashMap;

use super::{Coord, CoordType};
// use super::direction::Direction;

// const MOVES: HashMap<Direction, Pos> = HashMap::from([
// 	(Direction::Right, Pos::new( 1, 0)),
// 	(Direction::Left,  Pos::new(-1, 0)),
// 	(Direction::Down,  Pos::new(0,  1)),
// 	(Direction::Up,    Pos::new(0, -1)),
// ])

pub struct Pos {
	x: i32,
	y: i32,
}

impl Pos {
	pub fn new(x: i32, y: i32) -> Pos { return Pos{x, y} }
	pub fn x(&self) -> i32 { return self.x }
	pub fn y(&self) -> i32 { return self.y }
}

impl Coord for Pos{
	fn xc(&self) -> CoordType { return self.x.try_into().unwrap() }
	fn yc(&self) -> CoordType   { return self.y.try_into().unwrap() }
}

// fn (p *Pos) Add(other Pos) {
// 	// return Pos{p.x + other.x, p.y + other.y}
// 	p.x += other.x
// 	p.y += other.y
// }

// fn (p *Pos) Move(dirn dir.Direction) {
// 	move := moves[dirn]
// 	p.Add(move)
// }

// fn (p *Pos) Clone() Pos {
// 	return Pos{p.x, p.y}
// }

// fn (p *Pos) DirectionFrom(to grid.Coord) (dirn dir.Direction) {
// 	dx := to.X() - p.X()
// 	dy := to.Y() - p.Y()
// 	switch {
// 	case dx == -1 && dy == 0:
// 		dirn = dir.LEFT
// 	case dx == 1 && dy == 0:
// 		dirn = dir.RIGHT
// 	case dx == 0 && dy == -1:
// 		dirn = dir.UP
// 	case dx == 0 && dy == 1:
// 		dirn = dir.DOWN
// 	default:
// 		panic("Unexpected case")
// 	}
// 	return
// }

// --------------------
/*
const Y_FACTOR int = 10_000_000

type XYNode struct {
	Pos
}

fn NewNode(x, y int) XYNode {
	return XYNode{New(x, y)}
}

fn (n XYNode) ID() (id int64) {
	return GenerateID(n.x, n.y)
}

fn GenerateID(x, y int) (id int64) {
	return int64(y*Y_FACTOR + x)
}

fn (n *XYNode) Clone() XYNode {
	return XYNode{n.Pos}
}
*/