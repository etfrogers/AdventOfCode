use core::fmt;
use std::str::FromStr;

use utils::{
    self,
    grid::{pos::Pos, sparse::SparseGrid},
};

struct Line {
    from: Pos,
    to: Pos,
}

impl FromStr for Line {
    type Err = fmt::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut tokens = s.split(" -> ");
        let from = Pos::from_str(tokens.next().unwrap())?;
        let to = Pos::from_str(tokens.next().unwrap())?;
        Ok(Self { from, to })
    }
}

enum LineDir {
    Horz,
    Vert,
    Other,
}

impl Line {
    fn direction(&self) -> LineDir {
        if self.from.x() == self.to.x() {
            LineDir::Vert
        } else if self.from.y() == self.to.y() {
            LineDir::Horz
        } else {
            LineDir::Other
        }
    }

    fn iter(&self) -> LineIterator {
        LineIterator::new(&self)
    }
}

struct LineIterator<'a> {
    line: &'a Line,
    fixed_coord: i32,
    curr_move: i32,
    target: i32,
    inc: i32,
    exhausted: bool,
}

impl<'a> LineIterator<'a> {
    fn new(line: &'a Line) -> Self {
        let (fixed_coord, curr_move, target) = match line.direction() {
            LineDir::Horz => (line.from.y(), line.from.x(), line.to.x()),
            LineDir::Vert => (line.from.x(), line.from.y(), line.to.y()),
            LineDir::Other => (0, 0, 0),
        };
        let inc = if target > curr_move { 1 } else { -1 };
        Self {
            line,
            fixed_coord,
            curr_move,
            target,
            inc,
            exhausted: false,
        }
    }
}

impl<'a> Iterator for LineIterator<'a> {
    type Item = Pos;

    fn next(&mut self) -> Option<Self::Item> {
        if self.exhausted {
            return None;
        }
        if self.curr_move == self.target {
            self.exhausted = true;
        }
        let new_pos = match self.line.direction() {
            LineDir::Horz => Some(Pos::new(self.curr_move, self.fixed_coord)),
            LineDir::Vert => Some(Pos::new(self.fixed_coord, self.curr_move)),
            LineDir::Other => None,
        };
        self.curr_move += self.inc;
        new_pos
    }
}

struct VentMap {
    _lines: Vec<Line>,
    data: SparseGrid<u32>,
}

impl VentMap {
    pub fn build(input: Vec<String>) -> Self {
        let lines: Vec<_> = input.iter().map(|s| Line::from_str(s).unwrap()).collect();
        let mut data = SparseGrid::new();
        for line in lines.iter() {
            for coord in line.iter() {
                let count = data.entry(coord).or_insert(0);
                *count += 1
            }
        }
        Self {
            _lines: lines,
            data,
        }
    }

    fn n_overlaps(&self) -> u32 {
        self.data.values().map(|v| if *v > 1 { 1 } else { 0 }).sum()
    }
}

fn main() {
    let input = utils::input_lines(5);
    let vm = VentMap::build(input);

    let part_1_answer = vm.n_overlaps();
    println!("Day 5, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
