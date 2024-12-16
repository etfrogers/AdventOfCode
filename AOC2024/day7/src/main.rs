use itertools::{repeat_n, Itertools};
use std::{num::ParseIntError, str::FromStr};
use strum_macros::EnumIter;
use utils::{self, StringParseError};

struct Equation {
    target: u64,
    inputs: Vec<u64>,
}

struct Calibration(Vec<Equation>);

#[derive(Debug, EnumIter, Clone, Copy)]
enum Operator {
    Multiply,
    Add,
    Concatenate,
}

impl FromStr for Equation {
    type Err = StringParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (target, inputs) = s.split_once(":").ok_or(StringParseError::new(s))?;
        let target = target.parse().map_err(|_| StringParseError::new(target))?;
        let inputs = inputs
            .split_ascii_whitespace()
            .map(|v| v.parse())
            .collect::<Result<Vec<u64>, ParseIntError>>()
            .map_err(|_| StringParseError::new(inputs))?;
        Ok(Self { target, inputs })
    }
}

impl Equation {
    fn can_be_valid(&self, with_concat: bool) -> bool {
        let n_ops = self.inputs.len() - 1;
        // println!("");
        let mut all_ops = vec![Operator::Add, Operator::Multiply];
        if with_concat {
            all_ops.push(Operator::Concatenate)
        }
        for op_set in repeat_n(all_ops, n_ops).multi_cartesian_product() {
            // println!("{:?}", op_set);
            if self.apply_ops(op_set) == self.target {
                return true;
            }
        }
        false
    }

    fn apply_ops(&self, ops: Vec<Operator>) -> u64 {
        let mut result = self.inputs[0];

        for (op, val) in ops.iter().zip(self.inputs[1..].iter()) {
            result = match op {
                Operator::Add => result + val,
                Operator::Multiply => result * val,
                Operator::Concatenate => {
                    let mut s = result.to_string();
                    s.push_str(&val.to_string());
                    s.parse().unwrap()
                }
            };
            if result > self.target {
                return 0;
            }
        }
        result
    }
}

impl Calibration {
    fn new(input: Vec<String>) -> Self {
        Self(
            input
                .iter()
                .map(|s| Equation::from_str(s))
                .collect::<Result<Vec<Equation>, StringParseError>>()
                .unwrap(),
        )
    }

    fn _validity(&self, with_concat: bool) -> Vec<bool> {
        self.0.iter().map(|v| v.can_be_valid(with_concat)).collect()
    }

    fn total_calibration_result(&self, with_concat: bool) -> u64 {
        self.0
            .iter()
            .filter(|e| e.can_be_valid(with_concat))
            .map(|e| e.target)
            .sum()
    }
}

fn main() {
    let input = utils::input_lines(7);
    let cal = Calibration::new(input);
    let part_1_answer = cal.total_calibration_result(false);
    println!("Day 7, Part 1 answer: {}", part_1_answer);

    let part_2_answer = cal.total_calibration_result(true);
    println!("Day 7, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
