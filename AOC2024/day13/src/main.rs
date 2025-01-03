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
    fn build_list(input: Vec<String>, convert_units: bool) -> Vec<Self> {
        input
            .split(|line| line.is_empty())
            .map(|v| ClawMachine::build(v, convert_units))
            .collect()
    }

    fn build(input: &[String], convert_units: bool) -> Self {
        assert_eq!(input.len(), 3);
        let a = Button::from_str(&input[0]).unwrap();
        assert_eq!(a.label, "A");
        let b = Button::from_str(&input[1]).unwrap();
        assert_eq!(b.label, "B");
        let mut prize = Prize::from_str(&input[2]).unwrap();
        if convert_units {
            prize.convert_units();
        }
        Self { a, b, prize }
    }

    #[allow(non_snake_case)]
    fn n_presses(&self) -> Option<(u64, u64)> {
        let Ax = self.a.x as i64;
        let Bx = self.b.x as i64;
        let Ay = self.a.y as i64;
        let By = self.b.y as i64;
        let X = self.prize.x as i64;
        let Y = self.prize.y as i64;

        let det = (Ax * By) - (Bx * Ay);
        let a = (By * X - Bx * Y) / det;
        let b = (Y - a * Ay) / By;

        // println!("Before conversion: ({a}, {b})");
        let a = a.try_into().ok()?;
        let b = b.try_into().ok()?;
        if self.check(a, b) {
            // println!("Yup: {}, {}", a, b);
            Some((a, b))
        } else {
            // println!("Nope: {}, {}", a, b);
            None
        }
    }

    fn execute(&self, a: u64, b: u64) -> (u64, u64) {
        (a * self.a.x + b * self.b.x, a * self.a.y + b * self.b.y)
    }

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

impl Prize {
    fn convert_units(&mut self) {
        let conversion_factor = 10000000000000;
        self.x += conversion_factor;
        self.y += conversion_factor;
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
    let machines = ClawMachine::build_list(input.clone(), false);
    let part_1_answer = ClawMachine::total_cost(&machines);
    println!("Day 13, Part 1 answer: {}", part_1_answer);

    let machines = ClawMachine::build_list(input, true);
    let part_2_answer = ClawMachine::total_cost(&machines);
    println!("Day 13, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
