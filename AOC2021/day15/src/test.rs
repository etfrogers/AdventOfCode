use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_build(input: Vec<String>) {
    let rl = RiskLevel::build(input);
    assert_eq!(rl.map[(0, 0)], 1);
    assert_eq!(rl.map[(0, 2)], 2);
    assert_eq!(rl.map[(9, 9)], 1);
}

#[rstest]
fn test_path_finding(input: Vec<String>) {
    let rl = RiskLevel::build(input);
    let path = rl.find_lowest_risk_path().unwrap();
    assert_eq!(path.total_risk, 40)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(15);
    let rl = RiskLevel::build(input);
    let path = rl.find_lowest_risk_path().unwrap();
    let part_1_answer = path.total_risk;
    assert_eq!(part_1_answer, 621);
}
