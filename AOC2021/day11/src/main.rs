use core::fmt;
use std::{
    ops::{Deref, DerefMut},
    str::FromStr,
};

use utils::{self, grid::Grid};

struct Octopuses {
    data: Grid<u8>,
    n_flashes: u64,
}

impl Deref for Octopuses {
    type Target = Grid<u8>;

    fn deref(&self) -> &Self::Target {
        &self.data
    }
}

impl DerefMut for Octopuses {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.data
    }
}

impl Octopuses {
    fn build(input: Vec<String>) -> Self {
        Self {
            data: Octopuses::to_int(Grid::new_from_strings(input)),
            n_flashes: 0,
        }
    }

    fn to_int(str_grid: Grid<char>) -> Grid<u8> {
        str_grid.map(|s| String::from(*s).parse::<u8>().unwrap())
    }

    fn step(&mut self) {
        self.apply(|v| v + 1);
        let mut flashed = Grid::full(self.n_cols(), self.n_rows(), false);
        let mut new_flashes = true;
        while new_flashes {
            new_flashes = false;
            for c in self.coord_iter(false, false) {
                if self[c] > 9 && !flashed[c] {
                    new_flashes = true;
                    flashed[c] = true;
                    self.n_flashes += 1;
                    for n in self.neighbour_coords(&c, true) {
                        self[n] += 1;
                    }
                }
            }
        }
        self.coord_iter(false, false)
            .zip(flashed.iter())
            .for_each(|(c, elem_flashed)| {
                if *elem_flashed {
                    self[c] = 0
                }
            });
    }
}

impl FromStr for Octopuses {
    type Err = fmt::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self {
            data: Octopuses::to_int(Grid::from_str(s).unwrap()),
            n_flashes: 0,
        })
    }
}

fn main() {
    let input = utils::input_lines(11);
    let mut octs = Octopuses::build(input);
    for _ in 0..100 {
        octs.step();
    }
    let part_1_answer = octs.n_flashes;
    println!("Day 11, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
