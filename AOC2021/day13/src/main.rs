use core::fmt;
use lazy_static::lazy_static;
use regex::Regex;
use std::{fmt::Display, str::FromStr};

use utils::{
    self,
    grid::{pos::Pos, sparse::SparseGrid, GridTrait},
};

#[derive(Debug, PartialEq, Eq)]
enum Orientation {
    X,
    Y,
}

impl FromStr for Orientation {
    type Err = fmt::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "x" => Ok(Orientation::X),
            "y" => Ok(Orientation::Y),
            _ => Err(fmt::Error),
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
struct Fold {
    orientation: Orientation,
    coord: i32,
}

lazy_static! {
    static ref FOLD_RE: Regex = Regex::new(r"fold along (\w)=(\d+)").unwrap();
}

impl FromStr for Fold {
    type Err = fmt::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let Some(matches) = FOLD_RE.captures(s) else {
            return Err(fmt::Error);
        };
        let orientation = Orientation::from_str(&matches.get(1).unwrap().as_str())?;
        let coord = matches
            .get(2)
            .unwrap()
            .as_str()
            .parse()
            .map_err(|_| fmt::Error)?;
        Ok(Self { orientation, coord })
    }
}

fn parse_input(input: Vec<String>) -> (Vec<Pos>, Vec<Fold>) {
    let mut tokens = input.split(|s| s == "");
    let coords = tokens.next().unwrap();
    let folds = tokens.next().unwrap();
    let coords = coords.iter().map(|l| Pos::from_str(&l).unwrap()).collect();
    let folds = folds.iter().map(|s| Fold::from_str(s).unwrap()).collect();
    (coords, folds)
}

struct Paper {
    dots: SparseGrid<bool>,
}

impl Paper {
    fn build(coords: &Vec<Pos>) -> Self {
        let mut dots: SparseGrid<bool> = SparseGrid::new();
        for key in coords {
            dots.insert(*key, true);
        }
        Self { dots }
    }

    fn fold(&mut self, fold: &Fold) {
        match fold.orientation {
            Orientation::X => {
                let left = self.dots.slice((..fold.coord, ..));
                let mut right = self.dots.slice((fold.coord + 1.., ..));
                let fold_line: SparseGrid<_> =
                    self.dots.slice((fold.coord..=fold.coord, ..)).into();
                assert!(fold_line.len() == 0 || !fold_line.values().all(|v| *v));

                let mut left: SparseGrid<_> = left.into();
                for (p, v) in &mut *right {
                    let new_x = fold.coord - (p.x() - fold.coord);
                    let folded_p = Pos::new(new_x, p.y());
                    left[folded_p] = *left.get(&folded_p).unwrap_or(&false) || *v;
                }
                drop(right);
                self.dots = left;
            }
            Orientation::Y => {
                let top = self.dots.slice((.., ..fold.coord));
                let mut bottom = self.dots.slice((.., fold.coord + 1..));
                let fold_line: SparseGrid<_> =
                    self.dots.slice((.., fold.coord..=fold.coord)).into();
                assert!(fold_line.len() == 0 || !fold_line.values().all(|v| *v));

                let mut top: SparseGrid<_> = top.into();
                for (p, v) in &mut *bottom {
                    let new_y = fold.coord - (p.y() - fold.coord);
                    let folded_p = Pos::new(p.x(), new_y);
                    top[folded_p] = *top.get(&folded_p).unwrap_or(&false) || *v;
                }
                drop(bottom);
                self.dots = top;
            }
        }
    }

    fn n_dots(&self) -> usize {
        let mut count = 0;
        for v in self.dots.values() {
            if *v {
                count += 1;
            }
        }
        count
    }
}

impl Display for Paper {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let blank = '.';
        let dot = '#';
        let mut disp: SparseGrid<_> = self.dots.map(|v| if *v { dot } else { blank });
        disp.set_default('.');
        write!(f, "{}", disp)
    }
}

fn main() {
    let input = utils::input_lines(13);
    let (coords, folds) = parse_input(input);
    let mut paper = Paper::build(&coords);
    // println!("{}\n\n", paper.n_dots());
    paper.fold(&folds[0]);
    // println!("{}", paper.n_dots());
    let part_1_answer = paper.n_dots();
    println!("Day 13, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
