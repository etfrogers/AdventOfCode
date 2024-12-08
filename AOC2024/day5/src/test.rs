use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_validity(input: Vec<String>) {
    let (rules, updates) = parse_input(input);
    assert_eq!(
        updates.valid_updates(&rules),
        vec![true, true, true, false, false, false]
    )
}

#[rstest]
fn test_checksum(input: Vec<String>) {
    let (rules, updates) = parse_input(input);
    assert_eq!(updates.checksum(&rules), 143)
}

#[rstest]
#[case(0, 61)]
#[case(1, 53)]
#[case(2, 29)]
fn test_middle_number(#[case] index: usize, #[case] expected: u32, input: Vec<String>) {
    let (_, updates) = parse_input(input);
    assert_eq!(updates.0[index].middle_number(), expected)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(5);
    let (rules, updates) = parse_input(input);
    let part_1_answer = updates.checksum(&rules);
    assert_eq!(part_1_answer, 4578);
}
