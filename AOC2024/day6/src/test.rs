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
    let gm = GuardMap::new(input);
    let visited = gm.find_path();
    assert_eq!(visited, 41)
}

#[rstest]
fn test_obstructions(input: Vec<String>) {
    let gm = GuardMap::new(input);
    assert_eq!(gm.find_n_obstructions(), 6);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(6);
    let gm = GuardMap::new(input);
    let part_1_answer = gm.find_path();
    assert_eq!(part_1_answer, 5404);
}


#[test]
fn test_part2() {
    let input = utils::input_lines(6);
    let gm = GuardMap::new(input);
    let part_2_answer = gm.find_n_obstructions();
    assert_eq!(part_2_answer, 1984);
}
