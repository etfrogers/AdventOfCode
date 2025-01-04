use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_build(input: Vec<String>) {
    let hallway = Hallway::new(11, 7, &input);
    // hallway.visualise();
    assert_eq!(hallway.quad_counts(), (4, 0, 2, 2));
}

#[rstest]
fn test_step(input: Vec<String>) {
    let mut hallway = Hallway::new(11, 7, &input);
    hallway.step(100);
    assert_eq!(hallway.quad_counts(), (1, 3, 4, 1));
    assert_eq!(hallway.safety_factor(), 12);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(14);
    let mut hallway = Hallway::new(101, 103, &input);
    hallway.step(100);
    let part_1_answer = hallway.safety_factor();
    assert_eq!(part_1_answer, 218433348);
}
