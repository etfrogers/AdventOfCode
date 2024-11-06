use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_parse(input: Vec<String>) {
    let (template, rules) = parse_input(input);
    // assert_eq!(template, vec!['N', 'N', 'C', 'B']);
    assert_eq!(template, "NNCB");
    assert_eq!(rules.first().unwrap().pair, "CH");
    assert_eq!(rules.first().unwrap().insert, 'B');
    assert_eq!(rules.last().unwrap().pair, "CN");
    assert_eq!(rules.last().unwrap().insert, 'C');
}

#[rstest]
fn test_apply(input: Vec<String>) {
    let (pattern, rules) = parse_input(input);
    let applied = apply_rules(pattern, &rules);
    assert_eq!(applied, "NCNBCHB");
}

#[rstest]
#[case(1, "NCNBCHB")]
#[case(2, "NBCCNBBBCBHCB")]
#[case(3, "NBBBCNCCNBBNBNBBCHBHHBCHB")]
#[case(4, "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")]
fn test_repeat(input: Vec<String>, #[case] n: usize, #[case] expected: &str) {
    let (pattern, rules) = parse_input(input);
    let applied = repeat_apply(pattern, &rules, n);
    assert_eq!(applied, expected);
}

#[rstest]
fn test_checksum(input: Vec<String>) {
    let (pattern, rules) = parse_input(input);
    let applied = repeat_apply(pattern, &rules, 10);
    assert_eq!(applied.len(), 3073);
    assert_eq!(checksum(&applied), 1588);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(14);
    let (pattern, rules) = parse_input(input);
    let applied = repeat_apply(pattern.clone(), &rules, 10);
    let part_1_answer = checksum(&applied);
    assert_eq!(part_1_answer, 2891);
}
