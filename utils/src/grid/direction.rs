use std::collections::HashMap;

use lazy_static::lazy_static;

use crate::grid::pos::Pos;

#[derive(PartialEq, Eq, Hash, Clone, Copy)]
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
    pub static ref ORTHOGONAL_MOVES: HashMap<Direction, Pos> = HashMap::from([
        (Direction::Right, Pos::new(1, 0)),
        (Direction::Left, Pos::new(-1, 0)),
        (Direction::Down, Pos::new(0, 1)),
        (Direction::Up, Pos::new(0, -1)),
    ]);
}

lazy_static! {
    pub static ref DIAGONAL_MOVES: HashMap<Direction, Pos> = HashMap::from([
        (Direction::NorthWest, Pos::new(-1, -1)),
        (Direction::NorthEast, Pos::new(-1, 1)),
        (Direction::SouthWest, Pos::new(1, -1)),
        (Direction::SouthEast, Pos::new(1, 1)),
    ]);
}

lazy_static! {
    pub static ref MOVES: HashMap<Direction, Pos> = {
        let mut m = ORTHOGONAL_MOVES.clone();
        m.extend(DIAGONAL_MOVES.iter());
        m
    };
}

impl Direction {
    pub fn turn_right(&mut self) {
        *self = match self {
            Direction::East => Direction::South,
            Direction::South => Direction::West,
            Direction::West => Direction::North,
            Direction::North => Direction::East,
            _ => todo!(),
        }
    }

    pub fn turn_left(&mut self) {
        todo!()
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
