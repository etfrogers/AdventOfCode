/*use std::{
    fmt,
    ops::{Add, Mul},
    str::FromStr,
};

use super::pos::Pos;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Coord {
    x: CoordType,
    y: CoordType,
}

impl Coord {
    pub fn new(x: CoordType, y: CoordType) -> Self {
        Self { x, y }
    }

    pub fn x(&self) -> usize {
        return self.x;
    }

    pub fn y(&self) -> usize {
        return self.y;
    }

    pub fn from(p: &Pos) -> Option<Self> {
        Some(Self {
            x: p.x().try_into().ok()?,
            y: p.y().try_into().ok()?,
        })
    }
}

impl FromStr for Coord {
    type Err = <Pos as FromStr>::Err;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let pos = Pos::from_str(&s)?;
        Self::from(&pos).ok_or(fmt::Error)
    }
}

impl Add<Pos> for Coord {
    type Output = Pos;

    fn add(self, rhs: Pos) -> Self::Output {
        let x: i32 = self.x().try_into().expect("Overflow error");
        let y: i32 = self.y().try_into().expect("Overflow error");
        Pos::new(x + rhs.x(), y + rhs.y())
    }
}

impl Mul<usize> for Coord {
    type Output = Self;

    fn mul(self, rhs: usize) -> Self::Output {
        Coord {
            x: self.x * rhs,
            y: self.y * rhs,
        }
    }
}
*/
