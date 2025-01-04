use std::{cell::OnceCell, str::FromStr, time::Duration};

use regex::Regex;
use utils::{
    self,
    grid::{
        pos::{Coord, Pos},
        Grid, GridTrait,
    },
    StringParseError,
};

struct Hallway {
    size: Coord,
    robots: Vec<Robot>,
}

struct Robot {
    pos: Coord,
    vel: Pos,
}

fn parse_group<T: FromStr>(
    i: usize,
    groups: &regex::Captures<'_>,
    err: &StringParseError,
) -> Result<T, StringParseError> {
    groups
        .get(i)
        .ok_or_else(|| err.clone())?
        .as_str()
        .parse::<T>()
        .map_err(|_| err.clone())
}

impl FromStr for Robot {
    type Err = StringParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let re_cell = OnceCell::new();
        let err = StringParseError::new(s);
        let re = re_cell.get_or_init(|| Regex::new(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)").unwrap());
        let groups: regex::Captures<'_> = re.captures(s).ok_or_else(|| err.clone())?;

        Ok(Self {
            pos: Coord::new(
                parse_group(1, &groups, &err)?,
                parse_group(2, &groups, &err)?,
            ),
            vel: Pos::new(
                parse_group(3, &groups, &err)?,
                parse_group(4, &groups, &err)?,
            ),
        })
    }
}

impl Robot {
    fn step(&mut self, n: usize, grid_size: Coord) {
        let shift = self.vel * n;
        let new_pos_unwrapped = self.pos + shift;

        self.pos = new_pos_unwrapped
            .try_modulo(grid_size)
            .unwrap()
            .try_into()
            .unwrap();
    }
}

impl Hallway {
    fn new(x: usize, y: usize, input: &[String]) -> Self {
        Self {
            size: Coord::new(x, y),
            robots: input.iter().map(|s| Robot::from_str(s).unwrap()).collect(),
        }
    }

    fn safety_factor(&self) -> usize {
        let (ul, ur, ll, lr) = self.quad_counts();
        ul * ur * ll * lr
    }

    fn quad_counts(&self) -> (usize, usize, usize, usize) {
        let mid_x = (self.size.x() - 1) / 2;
        let mid_y = (self.size.y() - 1) / 2;
        let mut n_lower_left = 0;
        let mut n_lower_right = 0;
        let mut n_upper_right = 0;
        let mut n_upper_left = 0;
        for robot in &self.robots {
            let x = robot.pos.x();
            let y = robot.pos.y();
            if x < mid_x && y < mid_y {
                n_upper_left += 1;
            } else if x > mid_x && y < mid_y {
                n_upper_right += 1;
            } else if x < mid_x && y > mid_y {
                n_lower_left += 1;
            } else if x > mid_x && y > mid_y {
                n_lower_right += 1;
            } else if x == mid_x || y == mid_y {
                // do nothing
            } else {
                panic!("Unhandled case")
            }
        }
        (n_upper_left, n_upper_right, n_lower_left, n_lower_right)
    }

    fn visualise(&self) {
        let mut grid = Grid::full(self.size.x(), self.size.y(), 0);
        for robot in &self.robots {
            grid[robot.pos] += 1;
        }
        println!(
            "{}",
            grid.map(|v| if *v > 0 {
                v.to_string().chars().next().unwrap()
            } else {
                '.'
            })
        )
    }

    fn step(&mut self, n: usize) {
        for r in &mut self.robots {
            r.step(n, self.size);
        }
    }

    fn centre_counts(&self) -> usize {
        let low_edge = (self.size.x() - 1) / 4;
        let high_edge = (self.size.y() - 1) * 3 / 4;
        let mut n = 0;
        for robot in &self.robots {
            let x = robot.pos.x();
            // let y = robot.pos.y();
            if x > low_edge && x < high_edge {
                n += 1;
            }
        }
        println!("{n}");
        n
    }
}

fn main() {
    let input = utils::input_lines(14);
    let mut hallway = Hallway::new(101, 103, &input);
    hallway.step(100);
    let part_1_answer = hallway.safety_factor();
    println!("Day 14, Part 1 answer: {}", part_1_answer);

    let mut hallway = Hallway::new(101, 103, &input);
    let n_robots = hallway.robots.len();
    for i in 0.. {
        if hallway.centre_counts() > n_robots / 3 {
            println!("\n=====================================================\n");
            println!("{i}");
            hallway.step(1);
            hallway.visualise();
            std::thread::sleep(Duration::from_millis(200));
        } else if i % 1000 == 0 {
            println!("{i}");
        }
    }
}

#[cfg(test)]
mod test;
