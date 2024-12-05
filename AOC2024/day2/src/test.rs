use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_safeness(input: Vec<String>) {
    let reports = Report::new_list(input);
    assert_eq!(
        reports.iter().map(|v| v.is_safe(false)).collect::<Vec<_>>(),
        [true, false, false, false, false, true]
    )
}

#[rstest]
fn test_safeness_damped(input: Vec<String>) {
    let reports = Report::new_list(input);
    assert_eq!(
        reports.iter().map(|v| v.is_safe(true)).collect::<Vec<_>>(),
        [true, false, false, true, true, true]
    )
}

#[rstest]
fn test_n_safe(input: Vec<String>) {
    let reports = Report::new_list(input);
    assert_eq!(n_safe(&reports, false), 2);
    assert_eq!(n_safe(&reports, true), 4);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(2);
    let reports = Report::new_list(input);
    let part_1_answer = n_safe(&reports, false);
    assert_eq!(part_1_answer, 402);
}

#[test]
fn test_part2() {
    let input = utils::input_lines(2);
    let reports = Report::new_list(input);
    let part_2_answer = n_safe(&reports, true);
    assert_eq!(part_2_answer, 455);
}
