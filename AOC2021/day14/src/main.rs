use lazy_static::lazy_static;
use std::{
    collections::{HashMap, HashSet},
    ops::{Add, AddAssign, Deref, DerefMut},
    str::FromStr,
};

use regex::Regex;
use utils::{self, Counter, StringParseError};

lazy_static! {
    static ref RULE_RE: Regex = Regex::new(r"([A-Z]{2}) -> ([A-Z])").unwrap();
}

type Rules = HashMap<String, Rule>;

struct Rule {
    re: Regex,
    insert: char,
}

impl FromStr for Rule {
    type Err = StringParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let groups = RULE_RE.captures(s).unwrap();
        let pair = groups[1].to_string();
        if groups.len() == 3 {
            Ok(Rule {
                re: Regex::new(&pair).unwrap(),
                // pair,
                insert: groups[2].chars().next().unwrap(),
            })
        } else {
            Err(StringParseError::new(s))
        }
    }
}

fn parse_input(input: Vec<String>) -> (String, Rules) {
    let pattern_str = input[0].clone();
    let rule_input = &input[2..];
    let rules = rule_input
        .iter()
        .map(|s| {
            let rule = Rule::from_str(s).unwrap();
            (rule.re.as_str().to_owned(), rule)
        })
        .collect();
    (pattern_str, rules)
}

fn apply_rules(mut pattern: String, rules: &Rules) -> String {
    let mut insertions: Vec<_> = Vec::new();
    for r in rules.values() {
        let mut start_ind = 0;
        while let Some(loc) = r.re.find_at(&pattern, start_ind) {
            start_ind = loc.start() + 1;
            insertions.push((start_ind, r.insert));
        }
    }
    insertions.sort_by(|a, b| a.0.cmp(&b.0));

    for (offset, insertion) in insertions.into_iter().enumerate() {
        pattern.insert(insertion.0 + offset, insertion.1);
    }
    pattern
}

fn repeat_apply(mut pattern: String, rules: &Rules, n: usize) -> String {
    for _ in 0..n {
        pattern = apply_rules(pattern, rules);
    }
    pattern
}

fn checksum(string: &str) -> u64 {
    checksum_of_map(&Counter::new(string.chars()))
}

#[derive(Debug, Clone, PartialEq)]
struct CountMap(CMType);
type CMType = HashMap<char, u64>;
type MemoArgs = (String, u64);
type MemoMap = HashMap<MemoArgs, CountMap>;

impl AddAssign for CountMap {
    fn add_assign(&mut self, rhs: Self) {
        for (key, value) in rhs.0 {
            let entry = self.entry(key).or_insert(0);
            *entry += value
        }
    }
}
impl Add for CountMap {
    fn add(self, rhs: Self) -> Self {
        let mut map = HashMap::new();
        let mut all_keys = HashSet::new();
        all_keys.extend(self.keys());
        all_keys.extend(rhs.keys());
        for key in all_keys {
            let entry = map.entry(key).or_insert(0);
            *entry += self.get(&key).unwrap_or(&0) + rhs.get(&key).unwrap_or(&0)
        }
        CountMap(map)
    }

    type Output = Self;
}

impl Deref for CountMap {
    type Target = HashMap<char, u64>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for CountMap {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

fn checksum_of_map(map: &CMType) -> u64 {
    let min_count = map.values().min().unwrap();
    let max_count = map.values().max().unwrap();
    max_count - min_count
}

fn build_counts(pattern: &str, rules: &Rules, n: u64) -> CountMap {
    let mut counts = CountMap(HashMap::new());
    let mut memo: MemoMap = HashMap::new();
    let n_pairs = pattern.len() - 1;
    let depth = n;

    for i in 0..n_pairs {
        let pair = &pattern[i..=i + 1];
        counts += pair_counts(pair, depth, rules, &mut memo);
        if i < n_pairs - 1 {
            *counts.get_mut(&pair.chars().nth(1).unwrap()).unwrap() -= 1;
        }
    }
    counts
}

fn pair_counts<'a>(pair: &'a str, depth: u64, rules: &Rules, memo: &'a mut MemoMap) -> CountMap {
    let memo_key = (pair.to_owned(), depth);
    if let Some(memoised) = memo.get(&memo_key) {
        memoised.clone()
    } else if depth == 0 {
        CountMap(Counter::new(pair.chars()).data())
    } else {
        let depth = depth - 1;

        if let Some(rule) = rules.get(pair) {
            let mut chars = pair.chars();
            let char1 = chars.next().unwrap();
            let char2 = chars.next().unwrap();
            let insert = rule.insert.to_string();
            let new_pair1 = char1.to_string() + &insert;
            let new_pair2 = insert + &char2.to_string();
            let mut new_counts = pair_counts(&new_pair1, depth, rules, memo)
                + pair_counts(&new_pair2, depth, rules, memo);
            *new_counts.get_mut(&rule.insert).unwrap() -= 1;
            memo.insert(memo_key, new_counts.clone());
            new_counts
        } else {
            let counts = CountMap(Counter::new(pair.chars()).data());
            for n in 0..=depth {
                memo.insert((pair.to_owned(), n), counts.clone());
            }
            counts
        }
    }
}

fn main() {
    let input = utils::input_lines(14);
    let (pattern, rules) = parse_input(input);
    let applied = repeat_apply(pattern.clone(), &rules, 10);
    let part_1_answer = checksum(&applied);
    println!("Day 14, Part 1 answer: {}", part_1_answer);

    let counts = build_counts(&pattern, &rules, 10);
    let part_1_answer = checksum_of_map(&counts);
    println!("Day 14, Part 1 answer, method 2: {}", part_1_answer);

    let counts = build_counts(&pattern, &rules, 40);
    let part_2_answer = checksum_of_map(&counts);
    println!("Day 14, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
