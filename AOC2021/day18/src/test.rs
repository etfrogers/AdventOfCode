use super::*;
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
fn test_explode(#[case] mut sfn: SnailfishNumber, #[case] expected: SnailfishNumber) {
    assert!(sfn.try_explode());
    assert_eq!(sfn, expected)
}

#[rstest]
// #[case("[10,1]", "[[5,5],1]")]
#[case("[9,1]", "[9,1]")]
fn test_split(#[case] mut sfn: SnailfishNumber, #[case] expected: SnailfishNumber) {
    assert!(!sfn.try_split());
    assert_eq!(sfn, expected);
    if let SnailfishNumber::Pair(ref mut a, _) = sfn {
        if let SnailfishNumber::Regular(ref mut val) = **a {
            *val += 1;
        }
    }
    assert!(sfn.try_split());
    let expected = SnailfishNumber::from_str("[[5,5],1]").unwrap();
    assert_eq!(sfn, expected);
}

#[rstest]
#[case(
    "[[[[4,3],4],4],[7,[[8,4],9]]]",
    "[1,1]",
    "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
)]
fn test_add_reduce(
    #[case] a: SnailfishNumber,
    #[case] b: SnailfishNumber,
    #[case] expected: SnailfishNumber,
) {
    let actual = a + b;
    assert_eq!(actual, expected)
}

#[rstest]
#[case("[[1,2],[[3,4],5]]", 143)]
#[case("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384)]
#[case("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445)]
#[case("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791)]
#[case("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137)]
#[case("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488)]
fn test_magnitude(#[case] sfn: SnailfishNumber, #[case] expected: u64) {
    assert_eq!(sfn.magnitude(), expected)
}

#[rstest]
#[case(
    "[1,1]
[2,2]
[3,3]
[4,4]",
    "[[[[1,1],[2,2]],[3,3]],[4,4]]"
)]
#[case(
    "[1,1]
[2,2]
[3,3]
[4,4]
[5,5]",
    "[[[[3,0],[5,3]],[4,4]],[5,5]]"
)]
#[case(
    "[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]",
    "[[[[5,0],[7,4]],[5,5]],[6,6]]"
)]
#[case(LONG_HW, "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")]
fn test_sum(#[case] hw: &str, #[case] expected: SnailfishNumber) {
    let hw = Homework::from_str(hw).unwrap();
    assert_eq!(hw.sum(), expected)
}

static LONG_HW: &str = "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]";

#[rstest]
#[case(1, "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]")]
#[case(2, "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]")]
#[case(3, "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]")]
fn test_sum_stages(#[case] n_steps: usize, #[case] expected: SnailfishNumber) {
    let hw = Homework::from_str(LONG_HW).unwrap();
    let hw = Homework(hw.0.into_iter().take(n_steps).collect());
    let actual = hw.sum();
    assert_eq!(
        actual, expected,
        "left == right failed\n  left: {}\n right: {}",
        actual, expected
    )
}

#[test]
fn test_part1() {
    let input = utils::input_lines(18);
    let hw = Homework::new(input);
    let hw_answer = hw.sum();
    let part_1_answer = hw_answer.magnitude();
    assert_eq!(part_1_answer, 4480);
}
