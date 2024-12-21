use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "2333133121414131402";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_parse(input: Vec<String>) {
    let dm = DiskMap::new(&input);
    assert_eq!(dm.to_string(), "00...111...2...333.44.5555.6666.777.888899")
}

#[rstest]
fn test_defrag(input: Vec<String>) {
    let dm = DiskMap::new(&input);
    assert_eq!(dm.defrag().to_string(), "0099811188827773336446555566")
}

#[rstest]
fn test_checksum(input: Vec<String>) {
    let dm = DiskMap::new(&input);
    assert_eq!(dm.defrag().checksum(), 1928)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(9);

    let part_1_answer = 0;
    assert_eq!(part_1_answer, 1);
}
