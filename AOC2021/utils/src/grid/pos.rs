use core::fmt;
use lazy_static::lazy_static;
use std::{
    collections::HashMap,
    ops::{Add, AddAssign, Div, DivAssign, Mul, MulAssign, Sub},
    str::FromStr,
};

use super::direction::Direction;

lazy_static! {
    pub static ref ORTHOGONAL_MOVES: HashMap<Direction, Pos> = HashMap::from([
        (Direction::Right, Pos::new(1, 0)),
        (Direction::Left, Pos::new(-1, 0)),
        (Direction::Down, Pos::new(0, 1)),
        (Direction::Up, Pos::new(0, -1)),
    ]);
}

lazy_static! {
    pub static ref DIAGONAL_MOVES: Vec<Pos> = Vec::from([
        Pos::new(-1, -1),
        Pos::new(-1, 1),
        Pos::new(1, -1),
        Pos::new(1, 1),
    ]);
}

pub type CoordType = usize;
pub type Coord = Pos<usize>;

impl Coord {
    pub fn from(p: &Pos<i32>) -> Option<Self> {
        Some(Self {
            x: p.x().try_into().ok()?,
            y: p.y().try_into().ok()?,
        })
    }

    pub fn as_pos(&self) -> Option<Pos<i32>> {
        Some(Pos {
            x: self.x().try_into().ok()?,
            y: self.y().try_into().ok()?,
        })
    }
}

impl Pos<i32> {
    pub fn from(p: &Coord) -> Option<Self> {
        Some(Self {
            x: p.x().try_into().ok()?,
            y: p.y().try_into().ok()?,
        })
    }

    pub fn as_coord(&self) -> Option<Coord> {
        Some(Coord {
            x: self.x().try_into().ok()?,
            y: self.y().try_into().ok()?,
        })
    }
}

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
pub struct Pos<T: num::PrimInt = i32> {
    x: T,
    y: T,
}

impl<T: num::PrimInt> Pos<T> {
    pub fn new(x: T, y: T) -> Self {
        return Pos { x, y };
    }

    pub fn x(&self) -> T {
        return self.x;
    }

    pub fn y(&self) -> T {
        return self.y;
    }

    pub fn tuple(&self) -> (T, T) {
        (self.x, self.y)
    }
}

impl<T> From<(T, T)> for Pos<T>
where
    T: num::PrimInt,
{
    fn from(value: (T, T)) -> Self {
        Pos::new(value.0, value.1)
    }
}

impl<T: num::PrimInt> Mul<T> for Pos<T> {
    type Output = Self;

    fn mul(self, rhs: T) -> Self::Output {
        Pos {
            x: self.x * rhs,
            y: self.y * rhs,
        }
    }
}

impl<T: num::PrimInt + MulAssign> MulAssign<T> for Pos<T> {
    fn mul_assign(&mut self, rhs: T) {
        self.x *= rhs;
        self.y *= rhs;
    }
}

impl<T: num::PrimInt> Div<T> for Pos<T> {
    type Output = Self;

    fn div(self, factor: T) -> Self {
        Pos {
            x: self.x / factor,
            y: self.y / factor,
        }
    }
}

impl<T: num::PrimInt + DivAssign> DivAssign<T> for Pos<T> {
    fn div_assign(&mut self, factor: T) {
        self.x /= factor;
        self.y /= factor;
    }
}

impl<T: num::PrimInt + FromStr> FromStr for Pos<T> {
    type Err = fmt::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut tokens = s.split(",");
        let x = tokens
            .next()
            .ok_or_else(|| fmt::Error)?
            .parse::<T>()
            .map_err(|_| fmt::Error)?;
        let y = tokens
            .next()
            .ok_or_else(|| fmt::Error)?
            .parse::<T>()
            .map_err(|_| fmt::Error)?;
        Ok(Self { x, y })
    }
}

impl<T: num::PrimInt> Add for Pos<T> {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        Pos {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
        }
    }
}

impl<T: num::PrimInt + AddAssign> AddAssign for Pos<T> {
    fn add_assign(&mut self, rhs: Self) {
        self.x += rhs.x;
        self.y += rhs.y;
    }
}

impl<T: num::PrimInt> Sub for Pos<T> {
    type Output = Self;

    fn sub(self, rhs: Self) -> Self::Output {
        Pos {
            x: self.x - rhs.x,
            y: self.y - rhs.y,
        }
    }
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
