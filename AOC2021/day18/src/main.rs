use std::fmt::Display;
use std::{fmt, u8};
use std::{ops::Add, str::FromStr};

use itertools::Itertools;
use lazy_static::lazy_static;
use regex::Regex;
use utils;

#[derive(Debug, PartialEq, Clone)]
enum SnailfishNumber {
    Pair(Box<SnailfishNumber>, Box<SnailfishNumber>),
    Regular(u8),
}

lazy_static! {
    static ref SAILFISH_RE: Regex =
        Regex::new(r"(^\[([0-9,\[\]]+),([0-9,\[\]]+)\]$)|(^[0-9]$)").unwrap();
}

impl SnailfishNumber {
    fn new_pair(a: SnailfishNumber, b: SnailfishNumber) -> Self {
        SnailfishNumber::Pair(Box::new(a), Box::new(b))
    }

    fn new_pair_of_regular(a: u8, b: u8) -> Self {
        SnailfishNumber::new_pair(SnailfishNumber::Regular(a), SnailfishNumber::Regular(b))
    }

    fn reduce(&mut self) {
        // println!("Reducing {}", self);
        loop {
            // println!("  {}", self);
            if self.try_explode() {
                continue;
            }
            if self.try_split() {
                continue;
            }
            break;
        }
        // println!("Finished reducing")
    }

    fn try_explode(&mut self) -> bool {
        let tgt = Self::dig(self, Dug::empty(), 0, 4, u8::MAX);
        if let Some(target) = tgt.target {
            // println!("    Exploding {}", target);
            if let SnailfishNumber::Pair(a, b) = target {
                if let SnailfishNumber::Regular(left_value) = **a {
                    if let SnailfishNumber::Regular(right_value) = **b {
                        if let Some(left_number) = tgt.left_number {
                            *left_number += left_value
                        }
                        if let Some(right_number) = tgt.right_number {
                            *right_number += right_value
                        }
                        *target = SnailfishNumber::Regular(0);
                    } else {
                        panic!("Target should be a pair of regular numbers")
                    }
                } else {
                    panic!("Target should be a pair of regular numbers")
                }
            } else {
                panic!("Target should be a pair of regular numbers")
            }
            true
        } else {
            false
        }
    }

    fn try_split(&mut self) -> bool {
        let tgt = Self::dig(self, Dug::empty(), 0, u8::MAX, 10);
        if let Some(target) = tgt.target {
            // println!("    Splitting {}", target);
            if let SnailfishNumber::Regular(old_val) = target {
                let (a, b) = halves(*old_val);
                *target = SnailfishNumber::new_pair_of_regular(a, b);
            } else {
                panic!("Target should be a regular number")
            }
            true
        } else {
            false
        }
    }

    fn dig<'a>(
        sfn: &'a mut SnailfishNumber,
        mut result: Dug<'a>,
        mut depth: u8,
        max_depth: u8,
        max_value: u8,
    ) -> Dug<'a> {
        // println!("Entering dig\nArgs: {sfn}\n      {result:?}\n      {depth}");
        if result.target.is_none() || result.right_number.is_none() {
            if result.target.is_none()
                && ((depth == max_depth && matches!(sfn, SnailfishNumber::Pair(_, _)))
                    || matches!(sfn, SnailfishNumber::Regular(a) if *a>=max_value))
            {
                // println!("!! Setting target to {sfn}");
                // println!("!! Current result: {result:?}");
                result.target = Some(sfn);
            } else {
                match sfn {
                    SnailfishNumber::Regular(ref mut val) => {
                        if result.target.is_some() {
                            if result.right_number.is_none() {
                                result.right_number = Some(val);
                            }
                        } else {
                            result.left_number = Some(val);
                        }
                    }
                    Self::Pair(ref mut a, b) => {
                        depth += 1;
                        result = Self::dig(&mut (*a), result, depth, max_depth, max_value);
                        result = Self::dig(&mut (*b), result, depth, max_depth, max_value);
                    }
                }
            }
        }
        // println!("Exiting dig\nArgs: \n      {result:?}\n      {depth}");
        result
    }

    fn magnitude(&self) -> u64 {
        match self {
            Self::Regular(n) => (*n).into(),
            Self::Pair(a, b) => 3 * a.magnitude() + 2 * b.magnitude(),
        }
    }
}

fn halves(val: u8) -> (u8, u8) {
    let a = val / 2;
    let b = if val % 2 == 0 { a } else { a + 1 };
    (a, b)
}

#[derive(Debug)]
struct Dug<'a> {
    left_number: Option<&'a mut u8>,
    right_number: Option<&'a mut u8>,
    target: Option<&'a mut SnailfishNumber>,
}

impl<'a> Dug<'a> {
    fn empty() -> Self {
        Self {
            left_number: None,
            right_number: None,
            target: None,
        }
    }
}

impl Add for SnailfishNumber {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        let mut new = SnailfishNumber::Pair(Box::new(self), Box::new(rhs));
        new.reduce();
        new
    }
}

impl FromStr for SnailfishNumber {
    type Err = fmt::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        if s.len() == 1 {
            Ok(SnailfishNumber::Regular(s.parse().map_err(|_| fmt::Error)?))
        } else {
            let inner1_start = 1;
            let mut inner1_end = 0;
            let mut inner2_start = 0;
            let inner2_end = s.len() - 1;
            let mut depth = 0;
            for (i, char) in s.chars().enumerate() {
                if i == 0 {
                    assert_eq!(char, '[');
                } else if i == s.len() - 1 {
                    assert_eq!(
                        depth, 0,
                        "depth should be zero at the end of parsing: actual value = {}",
                        depth
                    );
                    assert_eq!(char, ']');
                } else {
                    match char {
                        '[' => depth += 1,
                        ']' => depth -= 1,
                        ',' => {
                            if depth == 0 {
                                inner1_end = i;
                                inner2_start = i + 1;
                            }
                        }
                        _ => (),
                    }
                }
            }

            let inner1 = &s[inner1_start..inner1_end];
            let inner2 = &s[inner2_start..inner2_end];
            Ok(SnailfishNumber::new_pair(
                SnailfishNumber::from_str(inner1)?,
                SnailfishNumber::from_str(inner2)?,
            ))
        }
    }
}

impl Display for SnailfishNumber {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            SnailfishNumber::Regular(a) => write!(f, "{}", a),
            SnailfishNumber::Pair(a, b) => write!(f, "[{},{}]", *a, *b),
        }
    }
}

struct Homework(Vec<SnailfishNumber>);

impl Homework {
    fn new(input: &Vec<String>) -> Self {
        Homework(
            input
                .iter()
                .map(|s| SnailfishNumber::from_str(&s).unwrap())
                .collect(),
        )
    }

    fn sum(self) -> SnailfishNumber {
        self.0.into_iter().reduce(|a, b| a + b).unwrap()
    }

    fn max_mag_pairwise_sum(&self) -> u64 {
        self.0
            .iter()
            .permutations(2)
            .map(|sfns| (sfns[0].clone() + sfns[1].clone()).magnitude())
            .max()
            .unwrap()
    }
}

impl FromStr for Homework {
    type Err = fmt::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let data: Result<Vec<SnailfishNumber>, fmt::Error> =
            s.lines().map(|s| SnailfishNumber::from_str(s)).collect();
        Ok(Homework(data?))
    }
}

fn main() {
    let input = utils::input_lines(18);
    let hw = Homework::new(&input);
    let hw_answer = hw.sum();
    let part_1_answer = hw_answer.magnitude();
    println!("Day 18, Part 1 answer: {}", part_1_answer);

    let hw = Homework::new(&input);
    let part_2_answer = hw.max_mag_pairwise_sum();
    println!("Day 18, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
