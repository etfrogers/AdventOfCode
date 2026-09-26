use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
";

const TEST_2: &str = "#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_build(input: Vec<String>) {
    let _maze = Maze::new_from_strs(input);
    // println!("{:?}", maze);
}

#[rstest]
fn test_1(input: Vec<String>) {
    let maze = Maze::new_from_strs(input);
    assert_eq!(maze.find_shortest_path(), 7036)
}

#[rstest]
fn test_2() {
    let maze = Maze::new_from_strs(utils::string_input_lines(TEST_2));
    assert_eq!(maze.find_shortest_path(), 11048)
}

#[rstest]
fn test_part1() {
    let input = utils::input_lines(16);
    let maze = Maze::new_from_strs(input);
    let part_1_answer = maze.find_shortest_path();
    assert_eq!(part_1_answer, 79404);
}
