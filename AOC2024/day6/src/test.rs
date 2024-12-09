use rstest::{rstest, fixture};
use super::*;

const TEST_1: &str = "...";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}


#[test]
fn test_part1() {
    let input = utils::input_lines(6);

    let part_1_answer = 0;
    assert_eq!(part_1_answer, 1);
}
