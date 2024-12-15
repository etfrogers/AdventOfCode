use std::ops::Deref;

use utils::{
    self,
    grid::{direction::DIAGONAL_MOVES, pos::Pos, Grid, GridTrait},
};

struct Wordsearch(Grid<char>);

impl Wordsearch {
    fn new(input: Vec<String>) -> Self {
        Self(Grid::new_from_strings(input))
    }

    fn n_words(&self, word: &str) -> u32 {
        let chars: Vec<_> = word.chars().collect();
        let mut n = 0;
        for (p, c) in &self.0 {
            if *c == chars[0] {
                'dir: for nb in self.neighbour_coords(&p, true) {
                    if self[nb] == chars[1] {
                        let dir =
                            Pos::<i32>::try_from(nb).unwrap() - Pos::<i32>::try_from(p).unwrap();
                        for (i, c) in chars[2..].iter().enumerate() {
                            if let Ok(new_pos) = (nb + (dir * (i + 1))).try_into() {
                                if !self.is_inside(&new_pos) || self[new_pos] != *c {
                                    continue 'dir;
                                }
                            } else {
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

    fn n_x_mas(&self) -> u32 {
        let mut n = 0;
        let diags: Vec<Pos> = DIAGONAL_MOVES.values().copied().collect();
        for (p, c) in &self.0 {
            if *c == 'A' {
                let mut n_diags = 0;
                for dir in &diags {
                    if let Ok(nb) = (p + *dir).try_into() {
                        if self.is_inside(&nb) && self[nb] == 'M' {
                            if let Ok(opp_nb) = (p - *dir).try_into() {
                                if self.is_inside(&opp_nb) && self[opp_nb] == 'S' {
                                    n_diags += 1;
                                }
                            }
                        }
                    }
                }
                if n_diags == 2 {
                    n += 1;
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
    let part_2_answer = ws.n_x_mas();
    println!("Day 4, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
