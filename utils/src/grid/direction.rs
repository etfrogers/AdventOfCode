use std::fmt::{Debug, Display};

use lazy_static::lazy_static;
use rustc_hash::FxHashMap;
use strum_macros::{EnumIter, EnumString};
use thiserror::Error;

use crate::grid::pos::Pos;

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy, EnumString, EnumIter)]
pub enum Direction {
    North,
    East,
    South,
    West,
    NorthEast,
    SouthEast,
    SouthWest,
    NorthWest,
}

#[allow(non_upper_case_globals)]
impl Direction {
    pub const Up: Direction = Direction::North;
    pub const Down: Direction = Direction::South;
    pub const Left: Direction = Direction::West;
    pub const Right: Direction = Direction::East;
}

lazy_static! {
    pub static ref ORTHOGONAL_MOVES: FxHashMap<Direction, Pos> = FxHashMap::from_iter([
        (Direction::East, Pos::new(1, 0)),
        (Direction::West, Pos::new(-1, 0)),
        (Direction::South, Pos::new(0, 1)),
        (Direction::North, Pos::new(0, -1)),
    ]);
}

lazy_static! {
    pub static ref DIAGONAL_MOVES: FxHashMap<Direction, Pos> = FxHashMap::from_iter([
        (Direction::NorthWest, Pos::new(-1, -1)),
        (Direction::NorthEast, Pos::new(1, -1)),
        (Direction::SouthWest, Pos::new(-1, 1)),
        (Direction::SouthEast, Pos::new(1, 1)),
    ]);
}

lazy_static! {
    pub static ref MOVES: FxHashMap<Direction, Pos> = {
        let mut m = ORTHOGONAL_MOVES.clone();
        m.extend(DIAGONAL_MOVES.iter());
        m
    };
}

lazy_static! {
    static ref INVERSE_MOVES: FxHashMap<Pos, Direction> =
        FxHashMap::from_iter(MOVES.iter().map(|(k, v)| (*v, *k)));
}

impl Direction {
    pub fn turn_right(&mut self) {
        *self = Direction::right_of(*self);
    }

    pub fn turn_left(&mut self) {
        *self = Direction::left_of(*self);
    }

    pub fn left_of(dir: Self) -> Self {
        match dir {
            Direction::East => Direction::North,
            Direction::South => Direction::East,
            Direction::West => Direction::South,
            Direction::North => Direction::West,
            _ => todo!(),
        }
    }

    pub fn right_of(dir: Self) -> Self {
        match dir {
            Direction::East => Direction::South,
            Direction::South => Direction::West,
            Direction::West => Direction::North,
            Direction::North => Direction::East,
            _ => todo!(),
        }
    }

    pub fn left(&self) -> Self {
        Direction::left_of(*self)
    }

    pub fn right(&self) -> Self {
        Direction::right_of(*self)
    }

    pub fn opposite(&self) -> Self {
        match self {
            Direction::North => Direction::South,
            Direction::East => Direction::West,
            Direction::South => Direction::North,
            Direction::West => Direction::East,
            Direction::NorthEast => Direction::SouthWest,
            Direction::SouthEast => Direction::NorthWest,
            Direction::SouthWest => Direction::NorthEast,
            Direction::NorthWest => Direction::SouthEast,
        }
    }

    pub fn is_opposite(&self, other: &Direction) -> bool {
        *other == self.opposite()
    }

    pub fn adjacent(&self) -> (Self, Self) {
        match self {
            Direction::North => (Direction::NorthEast, Direction::NorthWest),
            Direction::East => (Direction::NorthEast, Direction::SouthEast),
            Direction::South => (Direction::SouthEast, Direction::SouthWest),
            Direction::West => (Direction::SouthWest, Direction::NorthWest),
            Direction::NorthEast => (Direction::North, Direction::East),
            Direction::SouthEast => (Direction::South, Direction::East),
            Direction::SouthWest => (Direction::South, Direction::West),
            Direction::NorthWest => (Direction::North, Direction::West),
        }
    }

    pub fn is_adjacent(&self, other: &Direction) -> bool {
        let adj = self.adjacent();
        *other == adj.0 || *other == adj.1
    }

    pub fn right_angles(&self) -> (Self, Self) {
        match self {
            Direction::North | Direction::South => (Direction::East, Direction::West),
            Direction::East | Direction::West => (Direction::South, Direction::North),
            Direction::NorthEast | Direction::SouthWest => {
                (Direction::NorthWest, Direction::SouthEast)
            }
            Direction::SouthEast | Direction::NorthWest => {
                (Direction::SouthWest, Direction::NorthEast)
            }
        }
    }

    pub fn is_right_angles(&self, other: &Direction) -> bool {
        let right_angles = self.right_angles();
        *other == right_angles.0 || *other == right_angles.1
    }

    pub fn direction_between(&self, other: &Direction) -> Result<Direction, NoIntermediate> {
        if self.is_right_angles(other) {
            let adj_s = self.adjacent();
            if other.is_adjacent(&adj_s.0) {
                Ok(adj_s.0)
            } else {
                debug_assert!(other.is_adjacent(&adj_s.1));
                Ok(adj_s.1)
            }
        } else {
            Err(NoIntermediate::new(*self, *other))
        }
    }
}

impl Display for Direction {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}

#[derive(Error, Debug)]
#[error("No angle found between {d1} and {d2}")]
pub struct NoIntermediate {
    d1: Direction,
    d2: Direction,
}

impl NoIntermediate {
    fn new(d1: Direction, d2: Direction) -> Self {
        Self { d1, d2 }
    }
}

#[derive(Debug, Error)]
#[error("Could not convert pos {pos} to a direction. Pos must be a unit vector")]
pub struct NoDirectionFound {
    pos: Pos,
    source: Option<anyhow::Error>,
}

impl NoDirectionFound {
    pub fn new(pos: Pos) -> Self {
        Self { pos, source: None }
    }
}

impl TryFrom<Pos<i32>> for Direction {
    type Error = NoDirectionFound;

    fn try_from(value: Pos) -> Result<Self, Self::Error> {
        INVERSE_MOVES
            .get(&value)
            .ok_or(NoDirectionFound::new(value))
            .copied()
    }
}
// static all: Vec<Direction> = []Direction{NORTH, EAST, SOUTH, WEST}

// func All() iter.Seq[Direction] {
// 	return func(yield func(Direction) bool) {
// 		for _, d := range all {
// 			if !yield(d) {
// 				return
// 			}
// 		}
// 	}
// }

// static ARROWS: HashMap<Direction, &str> = HashMap::from([
// 	(Direction::North, "^"),
// 	(Direction::South, "v"),
// 	(Direction::East, ">"),
// 	(Direction::West,  "<"),
// ]);

// stat invArrows map[string]Direction = utils.InvertMap(arrows)

// func (d Direction) ToArrowString() string {
// 	return arrows[d]
// }

// func FromArrowString(s string) Direction {
// 	return invArrows[s]
// }
