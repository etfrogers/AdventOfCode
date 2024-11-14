use assert_matches::assert_matches;
use std::{fmt, u8};
use std::{ops::Add, str::FromStr};

use lazy_static::lazy_static;
use regex::Regex;
use utils;

#[derive(Debug, PartialEq)]
enum SnailfishNumber {
    Pair(Box<SnailfishNumber>, Box<SnailfishNumber>),
    Regular(u8),
}

lazy_static! {
    static ref SAILFISH_RE: Regex =
        Regex::new(r"(^\[([0-9,\[\]]+),([0-9,\[\]]+)\]$)|(^[0-9]$)").unwrap();
}

impl SnailfishNumber {
    fn reduce(&mut self) {
        loop {
            if self.try_explode() {
                continue;
            }
            if self.try_split() {
                continue;
            }
            break;
        }
    }

    fn try_explode(&mut self) -> bool {
        let tgt = Self::dig(self, Dug::empty(), 0, 4, u8::MAX);
        if let Some(target) = tgt.target {
            // println!("{:?}", tgt);
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

    fn dig<'a>(
        sfn: &'a mut SnailfishNumber,
        // mut left_number: &Option<&'a mut u8>,
        mut result: Dug<'a>,
        mut depth: u8,
        max_depth: u8,
        max_value: u8,
    ) -> Dug<'a> {
        // println!("Entering dig\nArgs: {sfn:?}\n      {left_number:?}\n      {depth}");
        // let mut right_number: Option<&'a u8> = None;

        if result.target.is_some() && result.right_number.is_some() {
            return result;
        }

        if result.target.is_none() && depth == max_depth
            || matches!(sfn, SnailfishNumber::Regular(a) if *a>=max_value)
        {
            result.target = Some(sfn);
            result
        } else {
            // let mut result: Option<Dug> = None;
            match sfn {
                SnailfishNumber::Regular(_) => result,
                Self::Pair(ref mut a, b) => {
                    depth += 1;
                    if let SnailfishNumber::Regular(ref mut a) = **a {
                        if result.target.is_some() {
                            if result.right_number.is_none() {
                                result.right_number = Some(a);
                            }
                        } else {
                            result.left_number = Some(a);
                        }
                    } else {
                        result = Self::dig(&mut (*a), result, depth, max_depth, max_value);
                    }
                    if let SnailfishNumber::Regular(ref mut b) = **b {
                        if result.target.is_some() {
                            if result.right_number.is_none() {
                                result.right_number = Some(b);
                            }
                        }
                    } else {
                        result = Self::dig(&mut (*b), result, depth, max_depth, max_value);
                    }
                    result
                }
            }
        }
    }

    fn try_split(&mut self) -> bool {
        todo!()
    }

    fn magnitude(&self) -> u64 {
        match self {
            Self::Regular(n) => (*n).into(),
            Self::Pair(a, b) => 3 * a.magnitude() + 2 * b.magnitude(),
        }
    }
}

#[derive(Debug)]
struct Dug<'a> {
    left_number: Option<&'a mut u8>,
    right_number: Option<&'a mut u8>,
    // parent: &'a SnailfishNumber,
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
        SnailfishNumber::Pair(Box::new(self), Box::new(rhs))
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
            Ok(SnailfishNumber::Pair(
                Box::new(SnailfishNumber::from_str(inner1)?),
                Box::new(SnailfishNumber::from_str(inner2)?),
            ))
        }
    }
}

fn main() {
    let input = utils::input_lines(18);
    let part_1_answer = 0;
    println!("Day 18, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
