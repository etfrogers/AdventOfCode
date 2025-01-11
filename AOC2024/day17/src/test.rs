use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_run(input: Vec<String>) {
    let mut comp = Computer::build(&input);
    assert_eq!(comp.run(), "4,6,3,5,6,3,5,2,1,0")
}

#[rstest]
fn test_1() {
    let mut comp = Computer {
        reg_a: 0,
        reg_b: 0,
        reg_c: 9,
        program: Program::from_str("2,6").unwrap(),
        pointer: 0,
        output_buffer: Vec::new(),
    };
    assert_eq!(comp.run(), "");
    assert_eq!(comp.reg_b, 1)
}

#[rstest]
fn test_2() {
    let mut comp = Computer {
        reg_a: 10,
        reg_b: 0,
        reg_c: 0,
        program: Program::from_str("5,0,5,1,5,4").unwrap(),
        pointer: 0,
        output_buffer: Vec::new(),
    };
    assert_eq!(comp.run(), "0,1,2");
}

#[rstest]
fn test_3() {
    let mut comp = Computer {
        reg_a: 2024,
        reg_b: 0,
        reg_c: 0,
        program: Program::from_str("0,1,5,4,3,0").unwrap(),
        pointer: 0,
        output_buffer: Vec::new(),
    };
    assert_eq!(comp.run(), "4,2,5,6,7,7,7,7,3,1,0");
    assert_eq!(comp.reg_a, 0)
}

#[rstest]
fn test_4() {
    let mut comp = Computer {
        reg_a: 0,
        reg_b: 29,
        reg_c: 0,
        program: Program::from_str("1,7").unwrap(),
        pointer: 0,
        output_buffer: Vec::new(),
    };
    assert_eq!(comp.run(), "");
    assert_eq!(comp.reg_b, 26)
}

#[rstest]
fn test_5() {
    let mut comp = Computer {
        reg_a: 0,
        reg_b: 2024,
        reg_c: 43690,
        program: Program::from_str("4,0").unwrap(),
        pointer: 0,
        output_buffer: Vec::new(),
    };
    assert_eq!(comp.run(), "");
    assert_eq!(comp.reg_b, 44354)
}

#[rstest]
fn test_quine() {
    let input = utils::string_input_lines(
        "Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0",
    );
    let mut comp = Computer::build(&input);
    comp.reg_a = 117440;
    assert_eq!(comp.run(), "0,3,5,4,3,0");
    assert_eq!(comp.program.original_listing, vec![0, 3, 5, 4, 3, 0]);
    assert_eq!(comp.find_quine_brute_force(), 117440);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(17);
    let mut comp = Computer::build(&input);
    let part_1_answer = comp.run();
    assert_eq!(part_1_answer, "4,3,7,1,5,3,0,5,4");
}

#[test]
fn test_translation() {
    let part_1_answer = translated_prog(22817223);
    assert_eq!(part_1_answer, vec![4, 3, 7, 1, 5, 3, 0, 5, 4]);
}

#[rstest]
#[case(vec![4], 1)]
#[case(vec![5,4], 0b1010)]
#[case(vec![0, 5,4], 87)]
#[case(vec![4, 3, 7, 1, 5, 3, 0, 5, 4], 22817223)]
fn test_invert(#[case] prog: Vec<Register>, #[case] exp: Register) {
    let answers = invert_prog(&prog);
    assert!(answers.contains(&exp));
    for a in answers {
        assert_eq!(translated_prog(a), prog);
    }
}

#[rstest]
fn test_part2() {
    let input = utils::input_lines(17);
    let comp = Computer::build(&input);
    let part_2_answer = comp.find_quine();

    assert_eq!(part_2_answer, 190384615275535);
}
