use std::collections::{HashMap, HashSet};

use lazy_static::lazy_static;

enum LineState {
    Corrupted(char),
    Complete,
    Incomplete(Vec<char>),
}

lazy_static! {
    static ref PAIRS: HashMap<char, char> =
        HashMap::from([('{', '}'), ('(', ')'), ('[', ']'), ('<', '>')]);
}

lazy_static! {
    static ref CORRUPTION_SCORES: HashMap<char, u32> =
        HashMap::from([(')', 3), (']', 57), ('}', 1197), ('>', 25137),]);
}

lazy_static! {
    static ref COMPLETION_SCORES: HashMap<char, u64> =
        HashMap::from([(')', 1), (']', 2), ('}', 3), ('>', 4),]);
}

fn process_line(line: &str) -> LineState {
    let mut stack = Vec::with_capacity(line.len());
    let openers: HashSet<_> = PAIRS.keys().collect();
    let closers: HashSet<_> = PAIRS.values().collect();
    for c in line.chars() {
        match c {
            a if openers.contains(&a) => stack.push(c),
            a if closers.contains(&a) => {
                let matcher = stack.pop().unwrap();
                if c != PAIRS[&matcher] {
                    return LineState::Corrupted(c);
                }
            }
            _ => panic!("unexpected char: {}", c),
        }
    }
    if stack.is_empty() {
        LineState::Complete
    } else {
        stack.reverse();
        let missing_chars = stack.iter().map(|c| PAIRS[c]).collect();
        LineState::Incomplete(missing_chars)
    }
}

fn corruption_score(lines: &[String]) -> u32 {
    lines
        .iter()
        .map(|s| process_line(s))
        .map(|status| match status {
            LineState::Corrupted(c) => CORRUPTION_SCORES[&c],
            _ => 0,
        })
        .sum()
}

fn line_score(state: LineState) -> u64 {
    let mut score = 0;
    if let LineState::Incomplete(missing_chars) = state {
        for c in missing_chars {
            score *= 5;
            score += COMPLETION_SCORES[&c];
        }
        score
    } else {
        panic!("line_score only implemented for Incomplete")
    }
}

fn completion_score(lines: &[String]) -> u64 {
    let mut scores: Vec<_> = lines
        .iter()
        .map(|s: &String| process_line(s))
        .filter(|status| matches!(status, LineState::Incomplete(_)))
        .map(line_score)
        .collect();
    scores.sort();
    scores[(scores.len() - 1) / 2]
}

fn main() {
    let input = utils::input_lines(10);
    let part_1_answer = corruption_score(&input);
    println!("Day 10, Part 1 answer: {}", part_1_answer);
    let part_2_answer = completion_score(&input);
    println!("Day 10, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
