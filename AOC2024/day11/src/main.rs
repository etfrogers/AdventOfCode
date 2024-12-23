use std::{collections::HashMap, fmt::Display};

#[derive(Debug, Hash, PartialEq, Eq)]
struct MemoKey(Stone, usize);

type MemoType = HashMap<MemoKey, usize>;

#[derive(Default)]
struct Stones(Vec<Stone>);

#[derive(Debug, Hash, PartialEq, Eq, Clone, Copy)]
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

    fn single(s: Stone) -> Self {
        Self(vec![s])
    }

    fn pair(s1: Stone, s2: Stone) -> Self {
        Self(vec![s1, s2])
    }

    fn blink(&self, remaining_depth: usize, memo: &mut MemoType) -> usize {
        self.0.iter().map(|s| s.blink(remaining_depth, memo)).sum()
    }

    fn blinks(&mut self, n: usize) -> usize {
        let mut memo: MemoType = HashMap::new();
        self.0.iter().map(|s| s.blink(n, &mut memo)).sum()
    }
}

impl Stone {
    fn blink(&self, remaining_depth: usize, memo: &mut MemoType) -> usize {
        let memo_key = MemoKey(*self, remaining_depth);
        if let Some(memoised) = memo.get(&memo_key) {
            *memoised
        } else if remaining_depth == 0 {
            1
        } else {
            let n_digits = (self.0 as f64 + 0.1).log10().ceil() as u32;
            let stones = if self.0 == 0 {
                Stones::single(Stone(1))
            } else if n_digits % 2 == 0 {
                let factor = 10_u64.pow(n_digits / 2);
                let left = Stone(self.0 / factor);
                let right = Stone(self.0 - (left.0 * factor));
                Stones::pair(left, right)
            } else {
                Stones::single(Stone(self.0 * 2024))
            };
            let n = stones.blink(remaining_depth - 1, memo);
            memo.insert(memo_key, n);
            n
        }
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
    let part_1_answer = stones.blinks(25);
    println!("Day 11, Part 1 answer: {}", part_1_answer);

    let part_2_answer = stones.blinks(75);
    println!("Day 11, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
