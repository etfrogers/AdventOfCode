use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_total_score(input: Vec<String>) {
    let tm = TopoMap::new(input);
    let n = tm.total_score();
    assert_eq!(n, 36)
}

#[rstest]
fn test_total_rating(input: Vec<String>) {
    let tm = TopoMap::new(input);
    let n = tm.total_rating();
    assert_eq!(n, 81)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(10);
    let tm = TopoMap::new(input);

    let part_1_answer = tm.total_score();
    assert_eq!(part_1_answer, 698);
}

#[test]
fn test_part2() {
    let input = utils::input_lines(10);
    let tm = TopoMap::new(input);

    let part_2_answer = tm.total_rating();
    assert_eq!(part_2_answer, 1436);
}
