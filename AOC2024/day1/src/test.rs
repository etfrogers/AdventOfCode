use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "3   4
4   3
2   5
1   3
3   9
3   3";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_total_diff(input: Vec<String>) {
    let (l1, l2) = parse_input(input);
    assert_eq!(total_diff(&l1, &l2), 11)
}

#[rstest]
fn test_similarity_score(input: Vec<String>) {
    let (l1, l2) = parse_input(input);
    assert_eq!(similarity_score(&l1, &l2), 31)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(1);
    let (l1, l2) = parse_input(input);
    let part_1_answer = total_diff(&l1, &l2);
    assert_eq!(part_1_answer, 2113135);
}

#[test]
fn test_part2() {
    let input = utils::input_lines(1);
    let (l1, l2) = parse_input(input);
    let part_2_answer = similarity_score(&l1, &l2);
    assert_eq!(part_2_answer, 19097157);
}
