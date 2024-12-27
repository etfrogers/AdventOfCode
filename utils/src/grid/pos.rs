use std::{
    fmt::Display,
    num::TryFromIntError,
    ops::{Add, AddAssign, Div, DivAssign, Mul, MulAssign, Sub},
    str::FromStr,
};

use crate::StringParseError;

use super::direction::{Direction, MOVES};

pub type CoordType = usize;
pub type Coord = Pos<usize>;

impl TryFrom<Pos<i32>> for Coord {
    type Error = TryFromIntError;

    fn try_from(value: Pos<i32>) -> Result<Self, Self::Error> {
        Ok(Self {
            x: value.x().try_into()?,
            y: value.y().try_into()?,
        })
    }
}

impl TryFrom<Coord> for Pos<i32> {
    type Error = TryFromIntError;

    fn try_from(value: Coord) -> Result<Self, Self::Error> {
        Ok(Self {
            x: value.x().try_into()?,
            y: value.y().try_into()?,
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
        Pos { x, y }
    }

    pub fn x(&self) -> T {
        self.x
    }

    pub fn y(&self) -> T {
        self.y
    }

    pub fn tuple(&self) -> (T, T) {
        (self.x, self.y)
    }
}

impl Pos<i32> {
    pub fn move_(&mut self, dir: Direction) {
        *self += dir.into();
    }
}

impl Pos<usize> {
    pub fn move_(&mut self, dir: Direction) {
        self.try_move(dir)
            .expect("Failed to move due to integer range errors")
    }

    pub fn try_move(&mut self, dir: Direction) -> Result<(), TryFromIntError> {
        *self = self.add_dir(dir)?;
        Ok(())
    }

    pub fn add_dir(&self, dir: Direction) -> Result<Pos<usize>, TryFromIntError> {
        let mut new_val: Pos<i32> = (*self).try_into()?;
        new_val += dir.into();
        Ok(new_val.try_into()?)
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

impl Mul<usize> for Pos<i32> {
    type Output = Self;

    fn mul(self, factor: usize) -> Self::Output {
        let factor: i32 = factor.try_into().unwrap();
        self * factor
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
    type Err = StringParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut tokens = s.split(",");
        let x = tokens
            .next()
            .ok_or_else(|| StringParseError::new(s))?
            .parse::<T>()
            .map_err(|_| StringParseError::new(s))?;
        let y = tokens
            .next()
            .ok_or_else(|| StringParseError::new(s))?
            .parse::<T>()
            .map_err(|_| StringParseError::new(s))?;
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

impl<T: num::PrimInt> Sub<Pos<T>> for Pos<T> {
    type Output = Self;

    fn sub(self, rhs: Self) -> Self::Output {
        Pos {
            x: self.x - rhs.x,
            y: self.y - rhs.y,
        }
    }
}

impl Sub<Pos<i32>> for Pos<usize> {
    type Output = Pos<i32>;

    fn sub(self, rhs: Pos<i32>) -> Self::Output {
        let old: Pos<i32> = self.try_into().unwrap();
        old - rhs
    }
}

impl Add<Pos<i32>> for Pos<usize> {
    type Output = Pos<i32>;

    fn add(self, rhs: Pos<i32>) -> Self::Output {
        let old: Pos<i32> = self.try_into().unwrap();
        old + rhs
    }
}

impl From<Direction> for Pos {
    fn from(value: Direction) -> Self {
        MOVES[&value]
    }
}

impl<T: num::PrimInt + Display> Display for Pos<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "({}, {})", self.x(), self.y())
    }
}

// fn (p *Pos) Move(dirn dir.Direction) {
// 	move := moves[dirn]
// 	p.Add(move)
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
