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

#[test]
fn test_part1() {
    let input = utils::input_lines(17);
    let mut comp = Computer::build(&input);
    let part_1_answer = comp.run();
    assert_eq!(part_1_answer, "4,3,7,1,5,3,0,5,4");
}
