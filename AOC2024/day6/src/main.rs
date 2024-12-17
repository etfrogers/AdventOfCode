use rustc_hash::FxHashSet;
use std::str::FromStr;

use utils::{
    self,
    grid::{
        direction::Direction,
        pos::{Coord, Pos},
        Grid, GridFind, GridTrait,
    },
    StringParseError,
};

#[derive(Debug, Default, Clone, Copy, PartialEq)]
enum MapSquare {
    #[default]
    Empty,
    Blocked,
}

#[derive(Debug, PartialEq, Eq)]
enum GuardState {
    Walked,
    Turned,
    Outside,
}

impl FromStr for MapSquare {
    type Err = StringParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "^" | "." => Ok(Self::Empty),
            "#" => Ok(Self::Blocked),
            v => Err(StringParseError::new(v)),
        }
    }
}

#[derive(Debug, Clone)]
struct Guard {
    pos: Coord,
    dir: Direction,
}

#[derive(Clone, Debug)]
struct GuardMap {
    map: Grid<MapSquare>,
    guard: Guard,
}

impl GuardMap {
    fn new(input: Vec<String>) -> Self {
        let map = Grid::new_from_strings(input);
        let guard = Guard {
            pos: map.find('^').unwrap(),
            dir: Direction::Up,
        };
        let map = map.map(|c| MapSquare::from_str(&c.to_string()).unwrap());
        Self { map, guard }
    }

    fn find_n_obstructions(&self) -> usize {
        let mut candiates = 0;
        let orig_path = Self::find_path_map(&self.map, &self.guard).unwrap();
        let mut candidate_map = self.map.clone();
        for pos in orig_path.iter() {
            if self.map[*pos] == MapSquare::Empty {
                candidate_map[*pos] = MapSquare::Blocked;
                if Self::find_path_map(&candidate_map, &self.guard).is_none() {
                    candiates += 1;
                }
                candidate_map[*pos] = MapSquare::Empty;
            }
        }
        candiates
    }

    fn find_path(&self) -> usize {
        Self::find_path_map(&self.map, &self.guard).unwrap().len()
    }

    fn find_path_map(map: &Grid<MapSquare>, guard: &Guard) -> Option<FxHashSet<Coord>> {
        let mut visited: FxHashSet<(Coord, Direction)> = FxHashSet::default();
        let mut guard = guard.clone();
        loop {
            if !map.is_inside(&guard.pos) {
                break;
            }
            let new_key = (guard.pos, guard.dir);
            if visited.contains(&new_key) {
                return None;
            }
            if Self::walk_guard(map, &mut guard) == GuardState::Outside {
                break;
            }
            visited.insert(new_key);
        }
        let squares_only: FxHashSet<_> = visited.iter().map(|v| v.0).collect();
        Some(squares_only)
    }

    fn walk_guard(map: &Grid<MapSquare>, guard: &mut Guard) -> GuardState {
        let ahead = guard.pos + <Direction as Into<Pos<i32>>>::into(guard.dir);
        if let Ok(ahead) = ahead.try_into() {
            if map.is_inside(&ahead) && map[ahead] == MapSquare::Blocked {
                guard.dir.turn_right();
                return GuardState::Turned;
            }
            guard.pos = ahead;
            GuardState::Walked
        } else {
            GuardState::Outside
        }
    }
}

fn main() {
    let input = utils::input_lines(6);
    let gm = GuardMap::new(input);
    let part_1_answer = gm.find_path();
    println!("Day 6, Part 1 answer: {}", part_1_answer);

    let part_2_answer = gm.find_n_obstructions();
    println!("Day 6, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
