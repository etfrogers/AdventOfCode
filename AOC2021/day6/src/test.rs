use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "3,4,3,1,2";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[fixture]
fn school(input: Vec<String>) -> School {
    School::new(utils::csv_line(&input[0]).unwrap())
}

#[rstest]
fn test_build(school: School) {
    assert_eq!(school[3], 2);
    assert_eq!(school[2], 1);
    assert_eq!(school[1], 1);
}

#[rstest]
fn test_total_fish(mut school: School) {
    school.evolve(80);
    assert_eq!(school.total_fish(), 5934);
}

#[rstest]
fn test_total_fish2(mut school: School) {
    school.evolve(256);
    assert_eq!(school.total_fish(), 26984457539);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(6);
    let input = utils::csv_line(&input[0]).unwrap();
    let mut school = School::new(input);
    school.evolve(80);
    let part_1_answer = school.total_fish();
    assert_eq!(part_1_answer, 366057);
}

#[test]
fn test_part2() {
    let input = utils::input_lines(6);
    let input = utils::csv_line(&input[0]).unwrap();
    let mut school = School::new(input);
    school.evolve(256);
    let part_2_answer = school.total_fish();
    assert_eq!(part_2_answer, 1653559299811);
}
