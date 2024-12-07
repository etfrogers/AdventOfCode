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

#[test]
fn test_part1() {
    let input = utils::input_lines(4);

    let part_1_answer = 0;
    assert_eq!(part_1_answer, 1);
}
