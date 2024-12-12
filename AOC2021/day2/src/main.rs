use std::str::FromStr;

#[derive(Debug, PartialEq)]
enum Direction {
    Forward,
    Down,
    Up,
}

impl FromStr for Direction {
    type Err = ();
    fn from_str(input: &str) -> Result<Direction, Self::Err> {
        match input {
            "forward" => Ok(Direction::Forward),
            "up" => Ok(Direction::Up),
            "down" => Ok(Direction::Down),
            _ => Err(()),
        }
    }
}

struct Instruction {
    dir: Direction,
    distance: u32,
}

impl FromStr for Instruction {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut parts = s.split_ascii_whitespace();
        let dir = match parts.next() {
            Some(s) => Direction::from_str(s)?,
            None => return Err(()),
        };
        let distance: u32 = match parts.next() {
            Some(n) => n.parse().unwrap(),
            None => return Err(()),
        };
        Ok(Instruction { dir, distance })
    }
}

impl Instruction {
    fn from_strs(strs: &[String]) -> Vec<Instruction> {
        strs.iter()
            .map(|s| Instruction::from_str(s).unwrap())
            .collect()
    }
}

fn total_distances(instructions: &Vec<Instruction>) -> (u32, u32) {
    let mut depth = 0;
    let mut horz = 0;
    for inst in instructions {
        match inst.dir {
            Direction::Down => depth += inst.distance,
            Direction::Up => depth -= inst.distance,
            Direction::Forward => horz += inst.distance,
        }
    }
    (horz, depth)
}

fn distances_with_aim(instructions: &Vec<Instruction>) -> (u32, u32) {
    let mut depth = 0;
    let mut horz = 0;
    let mut aim = 0;
    for inst in instructions {
        match inst.dir {
            Direction::Down => aim += inst.distance,
            Direction::Up => aim -= inst.distance,
            Direction::Forward => {
                horz += inst.distance;
                depth += inst.distance * aim;
            }
        }
    }
    (horz, depth)
}
fn checksum(instructions: &Vec<Instruction>, part1: bool) -> u32 {
    let dists = if part1 {
        total_distances(instructions)
    } else {
        distances_with_aim(instructions)
    };
    dists.0 * dists.1
}

fn main() {
    let instructions = Instruction::from_strs(&utils::input_lines(2));
    let cs1 = checksum(&instructions, true);

    print!("Day 2 Part 1  answer: {cs1}");

    let cs2 = checksum(&instructions, false);
    print!("Day 2 Part 2  answer: {cs2}");
}

#[cfg(test)]
mod test {
    use super::*;
    use utils;

    #[test]
    fn test_total_dists() {
        let instructions = Instruction::from_strs(&utils::string_input_lines(TEST_DATA));
        let dists = total_distances(&instructions);
        assert_eq!((15, 10), dists)
    }

    #[test]
    fn test_total_dists_aim() {
        let instructions = Instruction::from_strs(&utils::string_input_lines(TEST_DATA));
        let dists = distances_with_aim(&instructions);
        assert_eq!((15, 60), dists)
    }

    #[test]
    fn test_checksum() {
        let instructions = Instruction::from_strs(&utils::string_input_lines(TEST_DATA));
        let cs = checksum(&instructions, true);
        assert_eq!(150, cs)
    }

    #[test]
    fn test_checksum2() {
        let instructions = Instruction::from_strs(&utils::string_input_lines(TEST_DATA));
        let cs = checksum(&instructions, false);
        assert_eq!(900, cs)
    }

    #[test]
    fn test_part1() {
        let instructions = Instruction::from_strs(&utils::input_lines(2));
        let cs = checksum(&instructions, true);
        assert_eq!(cs, 2322630)
    }

    #[test]
    fn test_part2() {
        let instructions = Instruction::from_strs(&utils::input_lines(2));
        let cs = checksum(&instructions, false);
        assert_eq!(cs, 2105273490)
    }

    const TEST_DATA: &str = "forward 5
down 5
forward 8
up 3
down 8
forward 2";
}
