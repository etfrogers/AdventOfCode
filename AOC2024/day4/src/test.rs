use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_n_words(input: Vec<String>) {
    let ws = Wordsearch::new(input);
    assert_eq!(ws.n_words("XMAS"), 18);
}

#[rstest]
fn test_n_x(input: Vec<String>) {
    let ws = Wordsearch::new(input);
    assert_eq!(ws.n_x_mas(), 9);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(4);
    let ws = Wordsearch::new(input);
    let part_1_answer = ws.n_words("XMAS");
    assert_eq!(part_1_answer, 2591);
}

#[test]
fn test_part2() {
    let input = utils::input_lines(4);
    let ws = Wordsearch::new(input);
    let part_2_answer = ws.n_x_mas();
    assert_eq!(part_2_answer, 1880);
}
