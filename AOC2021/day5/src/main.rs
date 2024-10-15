use core::fmt;
use std::{cmp::max, str::FromStr};

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

#[derive(Debug, PartialEq, Eq)]
enum LineDir {
    Horz,
    Vert,
    Diagonal,
}

impl Line {
    fn direction(&self) -> LineDir {
        if self.from.x() == self.to.x() {
            LineDir::Vert
        } else if self.from.y() == self.to.y() {
            LineDir::Horz
        } else {
            LineDir::Diagonal
        }
    }

    fn iter(&self) -> LineIterator {
        LineIterator::new(&self)
    }
}

struct LineIterator {
    curr_pos: Pos,
    target: Pos,
    inc: Pos,
    exhausted: bool,
}

impl LineIterator {
    fn new(line: &Line) -> Self {
        let mut inc = line.to - line.from;
        inc.div_assign(max(inc.x().abs(), inc.y().abs()));
        Self {
            // subtract inc below, so that we can add it at the start of next()
            curr_pos: line.from - inc,
            target: line.to,
            inc,
            exhausted: false,
        }
    }
}

impl Iterator for LineIterator {
    type Item = Pos;

    fn next(&mut self) -> Option<Self::Item> {
        if self.exhausted {
            return None;
        }
        self.curr_pos += self.inc;
        if self.curr_pos == self.target {
            self.exhausted = true;
        }
        Some(self.curr_pos)
    }
}

struct VentMap {
    _lines: Vec<Line>,
    data: SparseGrid<u32>,
}

impl VentMap {
    pub fn build(input: &Vec<String>, ignore_diagonal: bool) -> Self {
        let lines: Vec<_> = input.iter().map(|s| Line::from_str(s).unwrap()).collect();
        let mut data = SparseGrid::new();
        for line in lines.iter() {
            if ignore_diagonal && line.direction() == LineDir::Diagonal {
                continue;
            }
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
    let vm = VentMap::build(&input, true);
    let part_1_answer = vm.n_overlaps();
    println!("Day 5, Part 1 answer: {}", part_1_answer);

    let vm = VentMap::build(&input, false);
    let part_2_answer = vm.n_overlaps();
    println!("Day 5, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
