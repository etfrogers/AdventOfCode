use std::sync::LazyLock;

use regex::Regex;
use utils;

static MUL_RE: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap());

fn process_muls(input: Vec<String>) -> u64 {
    let input = &input.join(" ");
    MUL_RE
        .captures_iter(input)
        .map(|m| {
            m.get(1).unwrap().as_str().parse::<u64>().unwrap()
                * m.get(2).unwrap().as_str().parse::<u64>().unwrap()
        })
        .sum()
}

fn main() {
    let input = utils::input_lines(3);
    let part_1_answer = process_muls(input);
    println!("Day 3, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
