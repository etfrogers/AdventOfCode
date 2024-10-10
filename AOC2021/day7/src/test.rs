use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "16,1,2,0,4,2,7,1,2,14";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[fixture]
fn starts(input: Vec<String>) -> Vec<u64> {
    utils::csv_line(&input[0]).unwrap()
}

#[rstest]
#[case(1, 41)]
#[case(3, 39)]
#[case(10, 71)]
fn test_fuel(#[case] pos: u64, #[case] expected_fuel: u64, starts: Vec<u64>) {
    assert_eq!(fuel_to_get_to(&starts, pos, false), expected_fuel)
}

#[rstest]
#[case(2, 206)]
#[case(5, 168)]
fn test_fuel_with_extra(#[case] pos: u64, #[case] expected_fuel: u64, starts: Vec<u64>) {
    assert_eq!(fuel_to_get_to(&starts, pos, true), expected_fuel)
}

#[rstest]
#[case(16-5, 66)]
#[case(5-1, 10)]
fn test_sum_to_n(#[case] n: i64, #[case] expected_fuel: i64) {
    assert_eq!(sum_to_n(n), expected_fuel)
}
#[rstest]
fn test_min_pos(starts: Vec<u64>) {
    assert_eq!(minimum_fuel(&starts, false), (2, 37))
}

#[rstest]
fn test_min_pos_with_extra(starts: Vec<u64>) {
    assert_eq!(minimum_fuel(&starts, true), (5, 168))
}

#[rstest]
#[case(vec![1, 3, 2], 2, 2)]
#[case(vec![1, 500, 1001], 500, 1000)]
fn test_min_pos_manual(
    #[case] input: Vec<u64>,
    #[case] exp_min_pos: u64,
    #[case] exp_min_fuel: u64,
) {
    assert_eq!(minimum_fuel(&input, false), (exp_min_pos, exp_min_fuel))
}

#[test]
fn test_part1() {
    let input = utils::input_lines(7);
    let input: Vec<u64> = utils::csv_line(&input[0]).unwrap().into_iter().collect();

    let part_1_answer = minimum_fuel(&input, false);
    assert_eq!(part_1_answer, (345, 348996));
}

#[test]
fn test_part2() {
    let input = utils::input_lines(7);
    let input: Vec<u64> = utils::csv_line(&input[0]).unwrap().into_iter().collect();

    let part_1_answer = minimum_fuel(&input, true);
    assert_eq!(part_1_answer, (481, 98231647));
}
