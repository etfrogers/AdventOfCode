use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "11111
19991
19191
19991
11111";

const TEST_2: &str = "5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_build(input: Vec<String>) {
    let octs = Octopuses::build(input);
    assert_eq!(octs.to_string(), TEST_1.to_owned() + "\n")
}

#[rstest]
fn test_step() {
    let expected = "6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637
";
    let mut octs = Octopuses::from_str(TEST_2).unwrap();
    octs.step();
    assert_eq!(octs.to_string(), expected);
}

#[rstest]
fn test_step_multiple_simple(input: Vec<String>) {
    let mut octs = Octopuses::build(input);
    assert_eq!(octs.to_string(), TEST_1.to_owned() + "\n");
    octs.step();
    assert_eq!(
        octs.to_string(),
        "34543
40004
50005
40004
34543
"
    );
    octs.step();
    assert_eq!(
        octs.to_string(),
        "45654
51115
61116
51115
45654
"
    );
}

#[rstest]
fn test_step_multiple_complex() {
    let mut octs = Octopuses::build(utils::string_input_lines(TEST_2));
    assert_eq!(octs.to_string(), TEST_2.to_owned() + "\n");
    octs.step();
    assert_eq!(
        octs.to_string(),
        "6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637
"
    );
    octs.step();
    assert_eq!(
        octs.to_string(),
        "8807476555
5089087054
8597889608
8485769600
8700908800
6600088989
6800005943
0000007456
9000000876
8700006848
"
    );
}

#[rstest]
fn test_100_steps() {
    let mut octs = Octopuses::build(utils::string_input_lines(TEST_2));
    for _ in 0..100 {
        octs.step();
    }
    assert_eq!(
        octs.to_string(),
        "0397666866
0749766918
0053976933
0004297822
0004229892
0053222877
0532222966
9322228966
7922286866
6789998766
"
    );
    assert_eq!(octs.n_flashes, 1656);
}

#[rstest]
fn test_synchro() {
    let mut octs = Octopuses::build(utils::string_input_lines(TEST_2));
    assert_eq!(octs.find_synchronised_flashes(), 195)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(11);
    let mut octs = Octopuses::build(input);
    for _ in 0..100 {
        octs.step();
    }
    let part_1_answer = octs.n_flashes;
    assert_eq!(part_1_answer, 1681);
}
