use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_build(input: Vec<String>) {
    let map = VentMap::build(&input, true);
    assert_eq!(map._lines.len(), 10);
}

#[rstest]
fn test_overlaps(input: Vec<String>) {
    let map = VentMap::build(&input, true);
    assert_eq!(map.n_overlaps(), 5)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(5);
    let vm = VentMap::build(&input, true);

    let part_1_answer = vm.n_overlaps();
    assert_eq!(part_1_answer, 6397);
}

#[test]
fn test_part2() {
    let input = utils::input_lines(5);
    let vm = VentMap::build(&input, false);

    let part_1_answer = vm.n_overlaps();
    assert_eq!(part_1_answer, 22335);
}
