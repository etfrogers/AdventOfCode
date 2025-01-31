use std::{cell::OnceCell, collections::HashSet, fmt::Display, str::FromStr};

use anyhow::{bail, Ok};
use indexmap::IndexSet;
use utils::{
    self,
    grid::{direction::Direction, pos::Coord, Grid, GridFind, GridTrait},
    StringParseError,
};

struct Warehouse {
    map: Grid<Cell>,
    is_wide: bool,
}

#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, Hash)]
enum Cell {
    Wall,
    Box,
    LeftBox,
    RightBox,
    #[default]
    Empty,
    Robot,
}

impl Cell {
    fn is_pushable(&self) -> bool {
        let pushable_cell = OnceCell::new();
        let pushable = pushable_cell
            .get_or_init(|| HashSet::from([Cell::Box, Cell::Robot, Cell::LeftBox, Cell::RightBox]));
        pushable.contains(self)
    }
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
        let map: Grid<Cell> =
            Grid::new_from_strings(input).map(|s| Cell::from_str(&s.to_string()).unwrap());
        Self { map, is_wide }
    }

    fn widen_strings(input: Vec<String>) -> anyhow::Result<Vec<String>> {
        input.iter().map(|s| Self::widen_line(s)).collect()
    }

    fn widen_line(line: &str) -> anyhow::Result<String> {
        Ok(line
            .chars()
            .map(Self::widen_char)
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
        // println!("{}{dir}", self.map);
        let robot_pos = self.robot_pos();

        if dir.is_horizontal() || !self.is_wide {
            let mut end_push = robot_pos.add_dir(dir).unwrap();
            while self.map[end_push].is_pushable() {
                end_push.move_(dir);
            }
            if self.map[end_push] == Cell::Wall {
                // cannot move as will be blocked
                return;
            }
            debug_assert_eq!(self.map[end_push], Cell::Empty);

            while end_push != robot_pos {
                let prev = end_push.add_dir(-dir).unwrap();
                self.map[end_push] = self.map[prev];
                end_push = prev;
            }
            self.map[robot_pos] = Cell::Empty;
            // println!("Horizontal\n")
        } else {
            let mut next_push = IndexSet::from([robot_pos.add_dir(dir).unwrap()]);
            let mut end_push;
            let mut to_move = IndexSet::from([robot_pos]);
            let mut can_push = true;
            while !next_push.is_empty() && can_push {
                end_push = next_push;
                next_push = IndexSet::new();
                for p in &end_push {
                    let curr_cell = self.map[*p];

                    match curr_cell {
                        Cell::Wall => {
                            can_push = false;
                            break;
                        }
                        Cell::Box => {
                            to_move.insert(*p);
                            next_push.insert(p.add_dir(dir).unwrap());
                        }
                        Cell::LeftBox | Cell::RightBox => {
                            to_move.insert(*p);
                            let other_dir = if curr_cell == Cell::LeftBox {
                                Direction::East
                            } else {
                                Direction::West
                            };
                            let other_half = p.add_dir(other_dir).unwrap();
                            to_move.insert(other_half);
                            next_push.insert(p.add_dir(dir).unwrap());
                            next_push.insert(other_half.add_dir(dir).unwrap());
                        }
                        Cell::Empty => (),
                        Cell::Robot => (),
                    }
                }
            }
            // println!("Can push: {can_push}\n");
            if can_push {
                while let Some(pos) = to_move.pop() {
                    let into = pos.add_dir(dir).unwrap();
                    self.map[into] = self.map[pos];
                    self.map[pos] = Cell::Empty;
                }
                self.map[robot_pos] = Cell::Empty;
            }
        }
        // let _ = std::io::stdin().read_line(&mut String::new()).unwrap();
    }

    fn follow_instructions(&mut self, moves: &Moves) {
        for dir in &moves.0 {
            self.move_robot(*dir);
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
        let to_find = if self.is_wide {
            Cell::LeftBox
        } else {
            Cell::Box
        };
        self.map.find_all(to_find).map(|c| c.gps()).sum()
    }
}

fn build_warehouse(input: &[String], is_wide: bool) -> (Warehouse, Moves) {
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
    let (mut wh, moves) = build_warehouse(&input, false);
    wh.follow_instructions(&moves);
    let part_1_answer = wh.gps();
    println!("Day 15, Part 1 answer: {}", part_1_answer);

    let (mut wh, moves) = build_warehouse(&input, true);
    wh.follow_instructions(&moves);
    let part_2_answer = wh.gps();
    println!("Day 15, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
