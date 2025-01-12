use std::{fmt::Display, str::FromStr};

use anyhow::{bail, Ok};
use utils::{
    self,
    grid::{direction::Direction, pos::Coord, Grid, GridFind, GridTrait},
    StringParseError,
};

struct Warehouse {
    map: Grid<Cell>,
    is_wide: bool,
}

#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
enum Cell {
    Wall,
    Box,
    LeftBox,
    RightBox,
    #[default]
    Empty,
    Robot,
}

impl FromStr for Cell {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "@" => Ok(Self::Robot),
            "." => Ok(Self::Empty),
            "O" => Ok(Self::Box),
            "#" => Ok(Self::Wall),
            "[" => Ok(Self::LeftBox),
            "]" => Ok(Self::RightBox),
            _ => Err(StringParseError::new(s).into()),
        }
    }
}

impl Display for Cell {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let chr = match self {
            Cell::Wall => "#",
            Cell::Box => "O",
            Cell::Empty => ".",
            Cell::Robot => "@",
            Cell::LeftBox => "[",
            Cell::RightBox => "]",
        };
        write!(f, "{chr}")
    }
}
struct Moves(Vec<Direction>);

impl FromStr for Moves {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let moves: Result<Vec<_>, StringParseError> = s
            .chars()
            .map(|c| Direction::from_str(&c.to_string()))
            .collect();
        Ok(Self(moves?))
    }
}

impl Warehouse {
    fn new(mut input: Vec<String>, is_wide: bool) -> Self {
        if is_wide {
            input = Warehouse::widen_strings(input).unwrap();
        }
        let map: Grid<Cell> = Grid::new_from_strings(input)
            .map(|s| Cell::from_str(&s.to_string()).unwrap())
            .into();
        Self { map, is_wide }
    }

    fn widen_strings(input: Vec<String>) -> anyhow::Result<Vec<String>> {
        input.iter().map(|line| Self::widen_line(line)).collect()
    }

    fn widen_line(line: &String) -> anyhow::Result<String> {
        Ok(line
            .chars()
            .map(|c| Self::widen_char(c))
            .collect::<anyhow::Result<Vec<_>>>()?
            .join(""))
    }

    fn widen_char(c: char) -> anyhow::Result<String> {
        Ok(match c {
            '#' => "##",
            '.' => "..",
            '@' => "@.",
            'O' => "[]",
            _ => bail!("Failed to match char {c}"),
        }
        .to_string())
    }

    fn robot_pos(&self) -> Coord {
        self.map.find(Cell::Robot).unwrap()
    }

    fn move_robot(&mut self, dir: Direction) {
        if self.is_wide {
            todo!()
        }
        let robot_pos = self.robot_pos();
        let mut end_push = robot_pos.add_dir(dir).unwrap();
        while self.map[end_push] == Cell::Box || self.map[end_push] == Cell::Robot {
            end_push.move_(dir);
        }
        if self.map[end_push] == Cell::Wall {
            // cannot move as will be block
            return;
        }
        debug_assert_eq!(self.map[end_push], Cell::Empty);

        while end_push != robot_pos {
            let prev = end_push.add_dir(-dir).unwrap();
            self.map[end_push] = self.map[prev];
            end_push = prev;
        }
        self.map[robot_pos] = Cell::Empty;
    }

    fn follow_instructions(&mut self, moves: Moves) {
        for dir in moves.0 {
            self.move_robot(dir);
        }
    }
}

trait Gps {
    fn gps(&self) -> usize;
}
impl Gps for Coord {
    fn gps(&self) -> usize {
        100 * self.y() + self.x()
    }
}

impl Gps for Warehouse {
    fn gps(&self) -> usize {
        self.map.find_all(Cell::Box).map(|c| c.gps()).sum()
    }
}

fn build_warehouse(input: Vec<String>, is_wide: bool) -> (Warehouse, Moves) {
    let mut parts = input.split(|s| s.is_empty());
    let wh = Warehouse::new(parts.next().unwrap().to_vec(), is_wide);
    let moves = parts.next().unwrap();
    assert!(parts.next().is_none());
    let moves = moves.iter().map(|s| s.trim()).collect::<Vec<_>>().join("");
    let moves = Moves::from_str(&moves).unwrap();
    (wh, moves)
}

fn main() {
    let input = utils::input_lines(15);
    let (mut wh, moves) = build_warehouse(input, false);
    wh.follow_instructions(moves);
    let part_1_answer = wh.gps();
    println!("Day 15, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
