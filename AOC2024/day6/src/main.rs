use std::{collections::HashSet, str::FromStr};

use utils::{
    self,
    grid::{
        direction::Direction,
        pos::{Coord, Pos},
        Grid, GridTrait,
    },
    StringParseError,
};

#[derive(Debug, Default, Clone, Copy, PartialEq)]
enum MapSquare {
    #[default]
    Empty,
    Blocked,
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

struct Guard {
    pos: Coord,
    dir: Direction,
}

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

    fn find_path(&mut self) -> usize {
        let mut visited: HashSet<Coord> = HashSet::new();
        loop {
            if !self.map.is_inside(&self.guard.pos) {
                break;
            }
            visited.insert(self.guard.pos);
            if !self.walk_guard() {
                break;
            }
        }
        visited.len()
    }

    fn walk_guard(&mut self) -> bool {
        let ahead = self.guard.pos + <Direction as Into<Pos<i32>>>::into(self.guard.dir);
        if let Ok(ahead) = ahead.try_into() {
            if self.map.is_inside(&ahead) && self.map[ahead] == MapSquare::Blocked {
                self.guard.dir.turn_right();
                return true;
            }
            self.guard.pos = ahead;
            true
        } else {
            false
        }
    }
}

fn main() {
    let input = utils::input_lines(6);
    let mut gm = GuardMap::new(input);
    let part_1_answer = gm.find_path();
    println!("Day 6, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
