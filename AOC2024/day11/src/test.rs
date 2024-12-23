use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "125 17";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_n_blink(input: Vec<String>) {
    let mut stones = Stones::new(&input);
    assert_eq!(stones.to_string(), "125 17");
    stones.blinks(6);
    assert_eq!(
        stones.blinks(6),
        "2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2"
            .split_ascii_whitespace()
            .collect::<Vec<_>>()
            .len()
    );
}

#[rstest]
fn test_n_stones(input: Vec<String>) {
    let mut stones = Stones::new(&input);
    assert_eq!(stones.blinks(25), 55312)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(11);
    let mut stones = Stones::new(&input);
    let part_1_answer = stones.blinks(25);
    assert_eq!(part_1_answer, 189092);
}

#[test]
fn test_part2() {
    let input = utils::input_lines(11);
    let mut stones = Stones::new(&input);
    let part_2_answer = stones.blinks(75);
    assert_eq!(part_2_answer, 224869647102559);
}
