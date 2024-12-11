use std::{cell::RefCell, fmt, num::ParseIntError, u16};

use utils::grid;

#[derive(Clone)]
struct Board {
    numbers: grid::Grid<u16>,
    matched: grid::Grid<bool>,
}

impl Board {
    fn from_strs(s: Vec<String>) -> Result<Self, fmt::Error> {
        let numbers = grid::Grid::from(
            s.iter()
                .map(|s| s.split_whitespace().map(|x| x.parse()).collect())
                .collect::<Result<Vec<Vec<u16>>, ParseIntError>>()
                .map_err(|_| fmt::Error)?,
        );
        let (x, y) = (numbers.n_rows(), numbers.n_cols());
        Ok(Self {
            numbers,
            matched: grid::Grid::full(x, y, false),
        })
    }

    fn has_won(&self) -> bool {
        let row_win = self
            .matched
            .row_iter()
            .map(|row| row.iter().all(|x| *x))
            .any(|x| x);
        let col_win = self
            .matched
            .col_iter()
            .map(|col| col.iter().all(|x| **x))
            .any(|x| x);
        col_win || row_win
    }

    fn call_number(&mut self, n: u16) {
        if let Some(c) = self.numbers.find(n) {
            self.matched[c] = true;
        }
    }

    fn total_unmarked(&self) -> u16 {
        self.numbers
            .values()
            .zip(self.matched.values())
            .filter(|pair| !*pair.1)
            .map(|pair| *pair.0)
            .sum()
    }
}

struct Game {
    calls: Vec<u16>,
    boards: RefCell<Vec<Board>>,
}

struct Winner {
    board: Board,
    last_call: u16,
}

impl Game {
    fn from_strs(s: Vec<String>) -> Result<Self, fmt::Error> {
        let mut tokens = s.split(|x| x == &"");
        let calls = tokens.next().ok_or(fmt::Error)?.get(0).ok_or(fmt::Error)?;
        let boards = tokens
            .map(|b| Board::from_strs(b.to_vec()))
            .collect::<Result<Vec<Board>, fmt::Error>>()?;
        let calls: Vec<u16> = utils::csv_line(calls).map_err(|_| fmt::Error)?;

        Ok(Self {
            calls,
            boards: RefCell::new(boards),
        })
    }

    fn play_game(&mut self) -> Vec<Winner> {
        let n_boards = self.boards.borrow().len();
        let mut to_play: Vec<usize> = (0..n_boards).collect();
        let mut winners: Vec<Winner> = Vec::with_capacity(n_boards);
        for number in self.calls.iter() {
            to_play = Self::call_number_on(*number, &mut self.boards.borrow_mut(), to_play);
            let mut new_play = Vec::with_capacity(to_play.len());
            for board_ind in to_play {
                let boards = self.boards.borrow();
                let board = &boards[board_ind];
                if board.has_won() {
                    winners.push(Winner {
                        board: board.clone(),
                        last_call: *number,
                    });
                } else {
                    new_play.push(board_ind);
                }
            }
            to_play = new_play;
        }
        winners
    }

    fn call_number_on(n: u16, boards: &mut Vec<Board>, to_play: Vec<usize>) -> Vec<usize> {
        for b in boards.iter_mut() {
            b.call_number(n)
        }
        to_play
    }
}

fn main() {
    let input = utils::input_lines(4);
    let mut game = Game::from_strs(input).expect("Failed to build game");
    let winners = game.play_game();
    let winner = &winners[0];
    let part_1_answer = winner.board.total_unmarked() * winner.last_call;

    println!("Day 4, Part 1 answer: {}", part_1_answer);

    let last_winner = winners.last().unwrap();
    let part_2_answer = last_winner.board.total_unmarked() * last_winner.last_call;

    println!("Day 4, Part 1 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
