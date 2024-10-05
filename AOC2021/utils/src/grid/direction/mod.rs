
#[derive(PartialEq, Eq, Hash)]
pub enum Direction {
	North,
	East,
	South,
	West,
}

#[allow(non_upper_case_globals)]
impl Direction {
	pub const Up: Direction = Direction::North;
	pub const Down: Direction = Direction::South;
	pub const  Left: Direction = Direction::West;
	pub const  Right: Direction = Direction::East;
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
