use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";
const TEST_2: &str = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_mul_finding(input: Vec<String>) {
    assert_eq!(process_muls(&input), 161);
}

#[rstest]
fn test_conditional(input: Vec<String>) {
    assert_eq!(conditional_muls(&input), 161);
    assert_eq!(conditional_muls(&vec![TEST_2.to_string()]), 48);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(3);

    let part_1_answer = process_muls(&input);
    assert_eq!(part_1_answer, 192767529);
}

#[test]
fn test_part2() {
    let input = utils::input_lines(3);

    let part_2_answer = conditional_muls(&input);
    assert_eq!(part_2_answer, 104083373);
}
