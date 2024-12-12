use super::*;
use prog::{program, program2, program3};
use rstest::rstest;

const TEST_NEG: &str = "inp x
mul x -1";

const TEST_BINARY: &str = "inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2";

#[rstest]
#[case(0, 0)]
#[case(1, -1)]
#[case(-789, 789)]
fn test_negation(#[case] input: NumberType, #[case] output: NumberType) {
    let prog = utils::string_input_lines(TEST_NEG);
    let alu = Alu::new();
    let prog = Program::build(prog, &alu);
    prog.run(vec![input]);
    assert_eq!(*alu.x.borrow(), output);
}

#[rstest]
#[case(8, &[1, 0, 0, 0])]
#[case(15, &[1, 1, 1, 1])]
#[case(1, &[0, 0, 0, 1])]
#[case(0, &[0, 0, 0, 0])]
fn test_binary(#[case] input: NumberType, #[case] output: &[NumberType]) {
    let prog = utils::string_input_lines(TEST_BINARY);
    let alu = Alu::new();
    let prog = Program::build(prog, &alu);
    prog.run(vec![input]);
    assert_eq!(*alu.w.borrow(), output[0]);
    assert_eq!(*alu.x.borrow(), output[1]);
    assert_eq!(*alu.y.borrow(), output[2]);
    assert_eq!(*alu.z.borrow(), output[3]);
}

#[test]
fn test_hypothesis_part1() {
    let hypothesis = vec![4, 1, 2, 9, 9, 9, 9, 4, 8, 7, 9, 9, 5, 9];
    assert!(program3(&hypothesis));
    assert!(program2(VecDeque::from(hypothesis.clone())));
    assert!(program(VecDeque::from(hypothesis.clone())));

    let program = utils::input_lines(24);
    let alu = Alu::new();
    let program = Program::build(program, &alu);
    program.run(hypothesis);
    assert_eq!(*alu.z.borrow(), 0);
}

#[test]
fn test_hypothesis_part2() {
    let hypothesis = vec![1, 1, 1, 8, 9, 5, 6, 1, 1, 1, 3, 2, 1, 6];
    assert!(program3(&hypothesis));
    assert!(program2(VecDeque::from(hypothesis.clone())));
    assert!(program(VecDeque::from(hypothesis.clone())));

    let program = utils::input_lines(24);
    let alu = Alu::new();
    let program = Program::build(program, &alu);
    program.run(hypothesis);
    assert_eq!(*alu.z.borrow(), 0);
}
