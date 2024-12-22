use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "125 17";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_blink(input: Vec<String>) {
    let mut stones = Stones::new(&input);
    assert_eq!(stones.to_string(), "125 17");
    stones.blink();
    assert_eq!(stones.to_string(), "253000 1 7");
    stones.blink();
    assert_eq!(stones.to_string(), "253 0 2024 14168");
}

#[rstest]
fn test_n_blink(input: Vec<String>) {
    let mut stones = Stones::new(&input);
    assert_eq!(stones.to_string(), "125 17");
    stones.blinks(6);
    assert_eq!(
        stones.to_string(),
        "2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2"
    );
}

#[rstest]
fn test_n_stones(input: Vec<String>) {
    let mut stones = Stones::new(&input);
    stones.blinks(25);
    assert_eq!(stones.len(), 55312)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(11);
    let mut stones = Stones::new(&input);
    stones.blinks(25);
    let part_1_answer = stones.len();
    assert_eq!(part_1_answer, 189092);
}
