use std::{cell::RefCell, fmt, num::ParseIntError, u16};

use utils::grid;

#[derive(Clone)]
struct Board {
    numbers: grid::Grid<u16>,
    matched: grid::Grid<bool>,
}

impl Board {

    fn from_strs(s: Vec<String>) -> Result<Self, fmt::Error> {
        let numbers = grid::Grid::new_from(s.iter()
            .map(|s| s.split_whitespace().map(|x| x.parse()).collect())
            .collect::<Result<Vec<Vec<u16>>, ParseIntError>>()
            .map_err(|_| fmt::Error)?
        );
        let (x, y) = (numbers.n_rows(), numbers.n_cols());
        Ok(Self{
            numbers,
            matched: grid::Grid::full(x, y, false)
        })
    }

    fn has_won(&self) -> bool {
        let row_win = self.matched
            .row_iter()
            .map(|row| row.iter().all(|x| *x))
            .any(|x| x);
        let col_win = self.matched
        .col_iter()
        .map(|col| col.iter().all(|x| **x))
        .any(|x| x);
        col_win || row_win
    }

    fn call_number(&mut self, n: u16) {
        if let Some(c) = self.numbers.find_c(n) {
            self.matched.set_c(&c, true);
        }

    }

    fn total_unmarked(&self) -> u16 {
        self.numbers
            .iter()
            .zip(self.matched.iter())
            .filter(|pair| !*pair.1)
            .map(|pair| *pair.0)
            .sum()
    }
}

struct Game {
    calls: Vec<u16>,
    boards: RefCell<Vec<Board>>,
}


impl Game {

    fn from_strs(s: Vec<String>) -> Result<Self, fmt::Error> {
        let mut tokens = s.split(|x| x==&"");
        let calls = tokens.next().ok_or(fmt::Error)?.get(0).ok_or(fmt::Error)?;
        let boards = tokens
            .map(|b| Board::from_strs(b.to_vec()))
            .collect::<Result<Vec<Board>, fmt::Error>>()?;
        let calls: Vec<u16> = calls
            .split(',')
            .map(|s| s.parse::<u16>())
            .collect::<Result<Vec<u16>, ParseIntError>>()
            .map_err(|_| fmt::Error)?;


        Ok(Self{
            calls,
            boards: RefCell::new(boards),
        })
    }

    fn play_game<'a>(&mut self) -> Option<(Board, u16)> {

        for number in self.calls.iter() {
            // self.call_number(*number);
            self.call_number(*number);
            let boards = self.boards.borrow();
            let winning_boards: Vec<_> = boards.iter().filter(|b| b.has_won()).collect();
            match winning_boards.len() {
                0 => (),
                1 => return Some((winning_boards[0].clone(), *number)),
                _ => panic!("multiple boards won")
            };
        };
        None
    }

    fn call_number(&self, n: u16) {
        for b in self.boards.borrow_mut().iter_mut() {
            b.call_number(n)
        }
    }
}

fn main() {
    let input = utils::input_lines(14);
    let mut game = Game::from_strs(input).expect("Failed to build game");
    let (winner, last_call) = game.play_game().unwrap();

    let part_1_answer = winner.total_unmarked() * last_call;
    println!("Day 4, Part 1 answer: {}", part_1_answer);

}

#[cfg(test)]
mod test;

