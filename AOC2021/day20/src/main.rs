use core::fmt;
use itertools::Itertools;
use std::{ops::Deref, str::FromStr};

use utils::{
    self,
    grid::{Grid, GridTrait},
};

#[derive(Debug, Default, Clone, Copy, PartialEq, Hash, Eq)]
enum Pixel {
    #[default]
    DARK,
    LIGHT,
}

impl Pixel {
    fn to_int(&self) -> String {
        match self {
            Pixel::DARK => "0".to_string(),
            Pixel::LIGHT => "1".to_string(),
        }
    }
}

impl FromStr for Pixel {
    type Err = fmt::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "#" => Ok(Pixel::LIGHT),
            "." => Ok(Pixel::DARK),
            _ => Err(fmt::Error),
        }
    }
}

impl fmt::Display for Pixel {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let c = match self {
            Pixel::DARK => '.',
            Pixel::LIGHT => '#',
        };
        write!(f, "{}", c)
    }
}

struct EnhancementAlgorithm(Vec<Pixel>);

impl Deref for EnhancementAlgorithm {
    type Target = Vec<Pixel>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug, PartialEq)]
struct Image {
    data: Grid<Pixel>,
    outside: Pixel,
}

impl Deref for Image {
    type Target = Grid<Pixel>;

    fn deref(&self) -> &Self::Target {
        &self.data
    }
}

impl fmt::Display for Image {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.data)
    }
}

#[derive(Debug)]
struct Chunk(Grid<Pixel>);

impl Chunk {
    fn to_index(&self) -> usize {
        let strs = self.0.iter().map(|v| v.to_int()).join("");
        usize::from_str_radix(&strs, 2).unwrap()
    }
}

impl fmt::Display for Chunk {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl Image {
    fn new_from_strings(input: &[String]) -> Self {
        Image {
            data: Grid::new_from_strings(input.to_vec())
                .map(|s| Pixel::from_str(&s.to_string()).unwrap()),
            outside: Pixel::DARK,
        }
    }

    fn enhance(&mut self, algo: &EnhancementAlgorithm) {
        let old_size = self.size();
        let mut new = self.clone();

        new.insert_col_of(0, self.outside).unwrap();
        new.insert_col_of(old_size.1 + 1, self.outside).unwrap();
        new.insert_row_of(0, self.outside).unwrap();
        new.insert_row_of(old_size.0 + 1, self.outside).unwrap();

        let orig = new.clone();

        let (n_x, n_y) = new.size();
        for pos in new.coord_iter(false, false) {
            let x = pos.x();
            let y = pos.y();
            // if x == 0 || y == 0 || x == n_x - 1 || y == n_y - 1 {
            // continue;
            // }

            let x1 = (if x > 0 { x - 1 } else { x }).clamp(0, n_x - 1);
            let x2 = (x + 1).clamp(0, n_x - 1);
            let y1 = (if y > 0 { y - 1 } else { y }).clamp(0, n_y - 1);
            let y2 = (y + 1).clamp(0, n_y - 1);

            let mut index_chunk = Chunk(orig.slice((x1..=x2, y1..=y2)).into());
            // println!("Before:\n{index_chunk}");
            if x == 0 {
                index_chunk.0.insert_col_of(0, self.outside).unwrap()
            }
            if y == 0 {
                index_chunk.0.insert_row_of(0, self.outside).unwrap();
            }
            if x == n_x - 1 {
                index_chunk.0.insert_col_of(2, self.outside).unwrap()
            }
            if y == n_y - 1 {
                index_chunk.0.insert_row_of(2, self.outside).unwrap();
            }
            // println!("After:\n{index_chunk}\n");
            assert_eq!(index_chunk.0.size(), (3, 3));
            let index = index_chunk.to_index();

            // println!("{}", new);

            new[pos] = algo[index];
        }
        self.outside = match self.outside {
            Pixel::DARK => *algo.first().unwrap(),
            Pixel::LIGHT => *algo.last().unwrap(),
        };
        self.data = new;
    }
}

fn parse_input(input: Vec<String>) -> (EnhancementAlgorithm, Image) {
    let algo = EnhancementAlgorithm(
        input[0]
            .chars()
            .map(|s| Pixel::from_str(&s.to_string()).unwrap())
            .collect(),
    );
    assert_eq!(algo.len(), 512);
    assert_eq!(input[1], "");
    let img = Image::new_from_strings(&input[2..]);
    (algo, img)
}

fn main() {
    let input = utils::input_lines(20);
    let (algo, mut img) = parse_input(input);
    img.enhance(&algo);
    img.enhance(&algo);
    let part_1_answer = img.counter()[&Pixel::LIGHT];
    println!("Day 20, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
