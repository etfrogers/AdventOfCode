use std::ops::Deref;

use utils::{
    self,
    grid::{pos::Pos, Grid, GridTrait},
};

struct Wordsearch(Grid<char>);

impl Wordsearch {
    fn new(input: Vec<String>) -> Self {
        Self(Grid::new_from_strings(input))
    }

    fn n_words(&self, word: &str) -> u32 {
        let chars: Vec<_> = word.chars().collect();
        let mut n = 0;
        for p in self.coord_iter(false, false) {
            if self[p] == chars[0] {
                'dir: for nb in self.neighbour_coords(&p, true) {
                    if self[nb] == chars[1] {
                        let dir =
                            Pos::<i32>::try_from(nb).unwrap() - Pos::<i32>::try_from(p).unwrap();
                        for (i, c) in chars[2..].iter().enumerate() {
                            let new_pos = nb + (dir * (i + 1));
                            if !self.is_inside(&new_pos) || self[new_pos] != *c {
                                continue 'dir;
                            }
                        }
                        n += 1;
                    }
                }
            }
        }
        n
    }
}

impl Deref for Wordsearch {
    type Target = Grid<char>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn main() {
    let input = utils::input_lines(4);
    let ws = Wordsearch::new(input);
    let part_1_answer = ws.n_words("XMAS");
    println!("Day 4, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
