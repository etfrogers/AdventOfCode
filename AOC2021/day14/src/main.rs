use core::fmt;
use lazy_static::lazy_static;
use std::str::FromStr;

use regex::Regex;
use utils::{self, Counter};

lazy_static! {
    static ref RULE_RE: Regex = Regex::new(r"([A-Z]{2}) -> ([A-Z])").unwrap();
}

struct Rule {
    re: Regex,
    pair: String,
    insert: char,
}

impl FromStr for Rule {
    type Err = fmt::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let groups = RULE_RE.captures(s).unwrap();
        let pair = groups[1].to_string();
        if groups.len() == 3 {
            Ok(Rule {
                re: Regex::new(&pair).unwrap(),
                pair,
                insert: groups[2].chars().into_iter().next().unwrap(),
            })
        } else {
            Err(fmt::Error)
        }
    }
}

fn parse_input(input: Vec<String>) -> (String, Vec<Rule>) {
    let pattern_str = input[0].clone();
    let rule_input = &input[2..];
    let rules = rule_input
        .iter()
        .map(|s| Rule::from_str(s).unwrap())
        .collect();
    (pattern_str, rules)
}

fn apply_rules(mut pattern: String, rules: &Vec<Rule>) -> String {
    let mut insertions: Vec<_> = Vec::new();
    for r in rules {
        let mut start_ind = 0;
        while let Some(loc) = r.re.find_at(&pattern, start_ind) {
            start_ind = loc.start() + 1;
            insertions.push((start_ind, r.insert));
        }
    }
    insertions.sort_by(|a, b| a.0.cmp(&b.0));
    let mut offset = 0;
    for insertion in insertions {
        pattern.insert(insertion.0 + offset, insertion.1);
        offset += 1;
    }
    pattern
}

fn repeat_apply(mut pattern: String, rules: &Vec<Rule>, n: usize) -> String {
    for _ in 0..n {
        pattern = apply_rules(pattern, rules);
    }
    pattern
}

fn checksum(string: &String) -> u64 {
    let counts = Counter::new(string.chars());
    let min_count = counts.values().min().unwrap();
    let max_count = counts.values().max().unwrap();
    max_count - min_count
}

fn main() {
    let input = utils::input_lines(14);
    let (pattern, rules) = parse_input(input);
    let applied = repeat_apply(pattern.clone(), &rules, 10);
    let part_1_answer = checksum(&applied);
    println!("Day 14, Part 1 answer: {}", part_1_answer);

    let applied2 = repeat_apply(pattern, &rules, 40);
    let part_2_answer = checksum(&applied2);
    println!("Day 14, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
