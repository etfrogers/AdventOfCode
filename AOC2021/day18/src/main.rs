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
        let tgt = Self::dig(&self, None, 0, 4, u8::MAX);
        println!("{:?}", tgt.unwrap());
        false
        // let mut sn = self;
        // let mut depth = depth;
        // match sn {
        //     SnailfishNumber::Regular(_) => (),
        //     Self::Pair(a, b) => {
        //         depth += 1;
        //         sn = &mut *a
        //     }
        // };
        // false
    }

    fn dig<'a>(
        sfn: &'a SnailfishNumber,
        // parent: Option<&'a SnailfishNumber>,
        mut left_number: Option<&'a u8>,
        mut depth: u8,
        // pred: T,
        max_depth: u8,
        max_value: u8,
    ) -> Option<Dug<'a>>
// where
    //     T: Fn(&SnailfishNumber, u32) -> bool,
    {
        println!("Entering dig\nArgs: {sfn:?}\n      {left_number:?}\n      {depth}");
        // let mut depth = 0;
        // let mut left_number: Option<&'a u8> = None;
        let mut right_number: Option<&'a u8> = None;
        // let stack = vec![sfn];
        let current = sfn;
        // let mut result: Option<Dug> = None;
        // while stack.len() > 0 {

        // let current = *stack.last().unwrap();
        if depth == max_depth || matches!(current, SnailfishNumber::Regular(a) if *a>=max_value) {
            Some(Dug {
                left_number,
                right_number: None,
                // parent: parent.unwrap(),
                target: &current,
            })
        } else {
            match current {
                SnailfishNumber::Regular(_) => {
                    // left_number = Some(&a); // case where this is a match is handled above
                    None
                }
                Self::Pair(a, b) => {
                    depth += 1;
                    if let SnailfishNumber::Regular(a) = a.as_ref() {
                        left_number = Some(a);
                    } else {
                        // stack.push(a);
                        // continue;
                        let res = Self::dig(&(*a), left_number, depth, max_depth, max_value);
                        if res.is_some() {
                            return res;
                        }
                        // if let a =
                        //     Self::dig(&(*a), left_number, depth, max_depth, max_value)
                        // {
                        //     if res_left.left_number.is_none() {
                        //         res_left.left_number = left_number;
                        //     }
                        //     result = Some(res_left);
                        //     // break;
                        // }
                    }
                    if let SnailfishNumber::Regular(_) = b.as_ref() {
                        // left_number = Some(b);
                    } else {
                        let res = Self::dig(&(*b), left_number, depth, max_depth, max_value);
                        if res.is_some() {
                            return res;
                        }
                        // {
                        // if res_right.left_number.is_none() {
                        //     res_right.left_number = left_number;
                        // }
                        // result = Some(res_right);
                        // // break;
                    }
                    None
                }
            }
            //     None
        }
        // end of match pred loop
        // result
        // None
        // if pred(sfn, depth) {
        //     Some(Dug {
        //         left_number,
        //         right_number: None,
        //         parent: parent.unwrap(),
        //         target: &sfn,
        //     })
        // } else {
        //     match sfn {
        //         SnailfishNumber::Regular(a) => {
        //             left_number = Some(a); // case where this is a match is handled above
        //         }
        //         Self::Pair(a, b) => {
        //             depth += 1;
        //             let res_left = Self::dig(&(*a), Some(sfn), left_number, depth, &pred);
        //             if res_left.is_some() {
        //                 return res_left;
        //             }
        //             let res_right = Self::dig(&(*b), Some(sfn), left_number, depth, &pred);
        //             if res_right.is_some() {
        //                 return res_right;
        //             }
        //         }
        //     };
        //     None
        // }
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
    left_number: Option<&'a u8>,
    right_number: Option<&'a u8>,
    // parent: &'a SnailfishNumber,
    target: &'a SnailfishNumber,
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
