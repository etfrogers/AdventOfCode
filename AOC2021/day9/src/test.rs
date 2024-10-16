use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "2199943210
3987894921
9856789892
8767896789
9899965678";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_low_points(input: Vec<String>) {
    let hm = HeightMap::build(input);
    assert_eq!(hm.low_points().collect::<Vec<_>>(), vec![1, 0, 5, 5])
}

#[rstest]
fn test_risk_levels(input: Vec<String>) {
    let hm = HeightMap::build(input);
    assert_eq!(hm.risk_levels().collect::<Vec<_>>(), vec![2, 1, 6, 6])
}

#[rstest]
fn test_total_risk(input: Vec<String>) {
    let hm = HeightMap::build(input);
    assert_eq!(hm.total_risk(), 15)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(9);
    let hm = HeightMap::build(input);
    let part_1_answer = hm.total_risk();
    assert_eq!(part_1_answer, 526);
}
