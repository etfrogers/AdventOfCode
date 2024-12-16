use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_validity(input: Vec<String>) {
    let cal = Calibration::new(input);
    assert_eq!(
        cal._validity(false),
        vec![true, true, false, false, false, false, false, false, true]
    );

    assert_eq!(
        cal._validity(true),
        vec![true, true, false, true, true, false, true, false, true]
    );
}

#[rstest]
fn test_total(input: Vec<String>) {
    let cal = Calibration::new(input);
    assert_eq!(cal.total_calibration_result(false), 3749);
    assert_eq!(cal.total_calibration_result(true), 11387);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(7);
    let cal = Calibration::new(input);
    let part_1_answer = cal.total_calibration_result(false);
    assert_eq!(part_1_answer, 2501605301465);
}

#[test]
fn test_part2() {
    let input = utils::input_lines(7);
    let cal = Calibration::new(input);
    let part_1_answer = cal.total_calibration_result(true);
    assert_eq!(part_1_answer, 44841372855953);
}
