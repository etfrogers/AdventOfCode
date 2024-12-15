use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_parse(input: Vec<String>) {
    let _ = GuardMap::new(input);
}

#[rstest]
fn test_path(input: Vec<String>) {
    let mut gm = GuardMap::new(input);
    let visited = gm.find_path();
    assert_eq!(visited, 41)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(6);
    let mut gm = GuardMap::new(input);
    let part_1_answer = gm.find_path();
    assert_eq!(part_1_answer, 5404);
}
