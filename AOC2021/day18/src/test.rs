use super::*;
use assert_matches::assert_matches;
use rstest::{fixture, rstest};

const TEST_BUILD: &str = "[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_BUILD)
}

#[rstest]
fn test_build() {
    let numbers: Vec<_> = utils::string_input_lines(TEST_BUILD)
        .iter()
        .map(|s| SnailfishNumber::from_str(s).unwrap())
        .collect();

    let SnailfishNumber::Pair(ref ap, ref c) = numbers[1] else {
        panic!("failed to match")
    };
    let SnailfishNumber::Pair(ref a, ref b) = **ap else {
        panic!("failed to match")
    };
    assert_eq!(**a, SnailfishNumber::Regular(1));
    assert_eq!(**b, SnailfishNumber::Regular(2));
    assert_eq!(**c, SnailfishNumber::Regular(3));
    // assert_matches!(numbers[0](SnailfishNumber)
}

#[rstest]
fn test_add() {
    let in1 = SnailfishNumber::from_str("[1,2]").unwrap();
    let in2 = SnailfishNumber::from_str("[[3,4],5]").unwrap();
    let expected = SnailfishNumber::from_str("[[1,2],[[3,4],5]]").unwrap();
    println!("{:?}", expected);
    let actual = in1 + in2;
    assert_eq!(actual, expected);
}

#[rstest]
#[case("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]")]
#[case("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]")]
#[case("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]")]
#[case(
    "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
    "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
)]
#[case("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")]
fn test_explode(#[case] input_str: &str, #[case] expected: &str) {
    let mut sfn = SnailfishNumber::from_str(input_str).unwrap();
    assert!(sfn.try_explode());
    let expected = SnailfishNumber::from_str(expected).unwrap();
    assert_eq!(sfn, expected)
}

#[rstest]
#[case("[[1,2],[[3,4],5]]", 143)]
#[case("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384)]
#[case("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445)]
#[case("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791)]
#[case("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137)]
#[case("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488)]
fn test_magnitude(#[case] input: &str, #[case] expected: u64) {
    let sfn = SnailfishNumber::from_str(input).unwrap();
    assert_eq!(sfn.magnitude(), expected)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(18);

    let part_1_answer = 0;
    assert_eq!(part_1_answer, 1);
}
