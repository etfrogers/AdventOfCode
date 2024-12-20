use std::collections::HashSet;

use itertools::Itertools;
use utils::{
    self,
    grid::{Grid, GridFind, GridTrait, SparseGrid},
};

#[derive(Debug)]
struct Antennas(SparseGrid<char>);

#[derive(Debug)]
struct Antinodes(SparseGrid<Vec<char>>);

impl Antinodes {
    fn new() -> Self {
        Self(SparseGrid::new())
    }

    fn len(&self) -> usize {
        self.0.len()
    }
}

impl Antennas {
    fn new(input: Vec<String>) -> Self {
        Self(SparseGrid::from_dense(Grid::new_from_strings(input), '.').unwrap())
    }

    fn find_antinodes(&self) -> Antinodes {
        let mut antinodes = Antinodes::new();
        for ch in HashSet::<char>::from_iter(self.0.values().map(|v| *v)) {
            let positions = self.0.find_all(ch);
            for pair in positions.combinations(2) {
                let delta = pair[1] - pair[0];
                let node_positions = vec![pair[1] + delta, pair[0] - delta];
                for pos in node_positions {
                    if self.0.is_inside(&pos) {
                        antinodes.0.entry(pos).or_insert(Vec::new()).push(ch);
                    }
                }
            }
        }
        antinodes
    }
}

fn main() {
    let input = utils::input_lines(8);
    let ants = Antennas::new(input);
    let antinodes = ants.find_antinodes();
    let part_1_answer = antinodes.len();
    println!("Day 8, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
