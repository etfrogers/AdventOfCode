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
    assert_eq!(rules["CH"].insert, 'B');
    assert_eq!(rules["CN"].insert, 'C');
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

#[rstest]
#[case(1, "NCNBCHB")]
#[case(2, "NBCCNBBBCBHCB")]
#[case(3, "NBBBCNCCNBBNBNBBCHBHHBCHB")]
#[case(4, "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")]
fn test_build_counts(input: Vec<String>, #[case] n: u64, #[case] expected: &str) {
    let (pattern, rules) = parse_input(input);
    let actual_counts = build_counts(&pattern, &rules, n);
    let expected_counts = Counter::new(expected.chars());
    assert_eq!(*expected_counts, *actual_counts)
}

#[rstest]
fn test_build_counts_no_match(input: Vec<String>) {
    let (_, rules) = parse_input(input);
    let mut memo = MemoMap::new();
    let exp_map = CountMap(HashMap::from([('Q', 2)]));
    assert_eq!(pair_counts("QQ", 8, &rules, &mut memo), exp_map);
    assert_eq!(memo.len(), 8);
    assert_eq!(*memo.get(&("QQ".to_string(), 7)).unwrap(), exp_map);
    assert_eq!(*memo.get(&("QQ".to_string(), 1)).unwrap(), exp_map);
    assert_eq!(*memo.get(&("QQ".to_string(), 2)).unwrap(), exp_map);
    assert_eq!(*memo.get(&("QQ".to_string(), 0)).unwrap(), exp_map);
}

#[rstest]
fn test_build_counts_simple(input: Vec<String>) {
    let (_, rules) = parse_input(input);
    let mut memo = MemoMap::new();
    let exp_map = CountMap(HashMap::from([('N', 2), ('C', 1)]));
    assert_eq!(pair_counts("NN", 1, &rules, &mut memo), exp_map);
    assert_eq!(
        pair_counts("NN", 2, &rules, &mut memo),
        CountMap(HashMap::from([('N', 2), ('C', 2), ('B', 1)]))
    );
}

#[test]
fn test_part1() {
    let input = utils::input_lines(14);
    let (pattern, rules) = parse_input(input);
    let applied = repeat_apply(pattern.clone(), &rules, 10);
    let part_1_answer = checksum(&applied);
    assert_eq!(part_1_answer, 2891);
}

#[test]
fn test_part_count_builder() {
    let input = utils::input_lines(14);
    let (pattern, rules) = parse_input(input);
    let counts = build_counts(&pattern, &rules, 10);
    let part_1_answer = checksum_of_map(&counts);
    assert_eq!(part_1_answer, 2891);
}

#[test]
fn test_part_2() {
    let input = utils::input_lines(14);
    let (pattern, rules) = parse_input(input);
    let counts = build_counts(&pattern, &rules, 40);
    let part_2_answer = checksum_of_map(&counts);
    assert_eq!(part_2_answer, 4607749009683);
}
