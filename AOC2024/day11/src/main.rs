use std::fmt::Display;

use linked_list::LinkedList;

use utils;

struct Stones(LinkedList<Stone>);

struct Stone(u64);

impl Stones {
    fn new(input: &[String]) -> Self {
        assert_eq!(input.len(), 1);
        let input = &input[0];
        Self(
            input
                .split_ascii_whitespace()
                .map(|s| Stone(s.parse().unwrap()))
                .collect(),
        )
    }

    fn blink(&mut self) {
        let mut cursor = self.0.cursor_mut();
        cursor.move_next();
        while let Some(stone) = cursor.current() {
            let n_digits = (stone.0 as f64 + 0.1).log10().ceil() as u32;
            if stone.0 == 0 {
                stone.0 = 1;
            } else if n_digits % 2 == 0 {
                let factor = 10_u64.pow(n_digits / 2);
                let left = Stone(stone.0 / factor);
                let right = Stone(stone.0 - (left.0 * factor));
                *stone = left;
                let rest = cursor.split_after();
                let mut right_list = LinkedList::new();
                right_list.push_back(right);
                cursor.splice_after(right_list);
                cursor.move_next();
                cursor.splice_after(rest);
                // cursor.move_next();
            } else {
                stone.0 *= 2024;
            }
            cursor.move_next();
        }
    }

    fn blinks(&mut self, n: usize) {
        for _ in 0..n {
            self.blink();
        }
    }

    fn len(&self) -> usize {
        self.0.len()
    }
}

impl Display for Stones {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let a: Vec<_> = self.0.iter().map(|v| v.0.to_string()).collect();
        write!(f, "{}", a.join(" "))
    }
}

fn main() {
    let input = utils::input_lines(11);
    let mut stones = Stones::new(&input);
    stones.blinks(25);
    let part_1_answer = stones.len();
    println!("Day 11, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
