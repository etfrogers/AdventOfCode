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
    assert_eq!(
        dm.defrag_blocks().to_string(),
        "0099811188827773336446555566"
    )
}

#[rstest]
fn test_checksum(input: Vec<String>) {
    let dm = DiskMap::new(&input);
    assert_eq!(dm.defrag_blocks().checksum(), 1928)
}

#[rstest]
#[case(TEST_1, "00992111777.44.333....5555.6666.....8888..", 2858)]
#[case("1313165", "021......33333......", 169)]

fn test_files(#[case] input: &str, #[case] exp_str: &str, #[case] exp_checksum: u64) {
    let dm = DiskMap::new(&vec![input.to_owned()]);
    let defrag = dm.defrag_files();
    assert_eq!(defrag.to_string(), exp_str);
    assert_eq!(defrag.checksum(), exp_checksum)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(9);
    let dm = DiskMap::new(&input);
    let part_1_answer = dm.defrag_blocks().checksum();
    assert_eq!(part_1_answer, 6331212425418);
}

#[test]
fn test_part2() {
    let input = utils::input_lines(9);
    let dm = DiskMap::new(&input);
    let part_2_answer = dm.defrag_files().checksum();
    assert_eq!(part_2_answer, 6363268339304);
}
