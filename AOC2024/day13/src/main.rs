use std::{cell::OnceCell, str::FromStr};

use regex::Regex;
use utils::{self, StringParseError};

struct ClawMachine {
    a: Button,
    b: Button,
    prize: Prize,
}

struct Button {
    label: String,
    x: u64,
    y: u64,
}

struct Prize {
    x: u64,
    y: u64,
}

impl ClawMachine {
    fn build_list(input: Vec<String>) -> Vec<Self> {
        input
            .split(|line| line.is_empty())
            .map(ClawMachine::build)
            .collect()
    }

    fn build(input: &[String]) -> Self {
        assert_eq!(input.len(), 3);
        let a = Button::from_str(&input[0]).unwrap();
        assert_eq!(a.label, "A");
        let b = Button::from_str(&input[1]).unwrap();
        assert_eq!(b.label, "B");
        let prize = Prize::from_str(&input[2]).unwrap();
        Self { a, b, prize }
    }

    #[allow(non_snake_case)]
    fn n_presses(&self) -> Option<(u64, u64)> {
        let Ax = self.a.x as f64;
        let Bx = self.b.x as f64;
        let Ay = self.a.y as f64;
        let By = self.b.y as f64;
        let X = self.prize.x as f64;
        let Y = self.prize.y as f64;

        let a = (By * X - Bx * Y) / (Ax * By - Bx * Ay);

        if a.fract().abs() > 1e-6 {
            println!("NONE!");
            return None;
        }
        let b = (Y - a * Ay) / By;

        // println!(
        //     "{:?} -> {} => >? {}, <? {}",
        //     (a, b),
        //     a.fract(),
        //     a.fract() > 1e-6,
        //     a.fract() < 1e-6
        // );

        Some((a as u64, b as u64))
    }

    #[allow(dead_code)]
    fn execute(&self, a: u64, b: u64) -> (u64, u64) {
        (a * self.a.x + b * self.b.x, a * self.a.y + b * self.b.y)
    }

    #[allow(dead_code)]
    fn check(&self, a: u64, b: u64) -> bool {
        (self.prize.x, self.prize.y) == self.execute(a, b)
    }

    fn cost_to_win(&self) -> Option<u64> {
        if let Some((a_press, b_press)) = self.n_presses() {
            Some(3 * a_press + b_press)
        } else {
            None
        }
    }

    fn total_cost(machines: &[ClawMachine]) -> u64 {
        machines
            .iter()
            .map(|m| m.cost_to_win().unwrap_or_default())
            .sum()
    }
}

impl FromStr for Button {
    type Err = StringParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let re_cell = OnceCell::new();
        let err = StringParseError::new(s);
        let re = re_cell.get_or_init(|| Regex::new(r"Button ([A|B]): X\+(\d+), Y\+(\d+)").unwrap());
        let groups = re.captures(s).ok_or_else(|| err.clone())?;
        let get_group = |i| Ok(groups.get(i).ok_or_else(|| err.clone())?.as_str());
        let parse_group = |i| get_group(i)?.parse().map_err(|_| err.clone());
        let label = get_group(1)?.to_owned();
        let x = parse_group(2)?;
        let y = parse_group(3)?;
        Ok(Self { label, x, y })
    }
}

impl FromStr for Prize {
    type Err = StringParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let re_cell = OnceCell::new();
        let err = StringParseError::new(s);
        let re = re_cell.get_or_init(|| Regex::new(r"Prize: X=(\d+), Y=(\d+)").unwrap());
        let groups = re.captures(s).ok_or_else(|| err.clone())?;
        let get_group = |i| Ok(groups.get(i).ok_or_else(|| err.clone())?.as_str());
        let parse_group = |i| get_group(i)?.parse().map_err(|_| err.clone());
        let x = parse_group(1)?;
        let y = parse_group(2)?;
        Ok(Self { x, y })
    }
}

fn main() {
    let input = utils::input_lines(13);
    let machines = ClawMachine::build_list(input);
    let part_1_answer = ClawMachine::total_cost(&machines);
    println!("Day 13, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
