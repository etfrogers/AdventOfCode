use super::*;
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
    let alu = ALU::new();
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
    let alu = ALU::new();
    let prog = Program::build(prog, &alu);
    prog.run(vec![input]);
    assert_eq!(*alu.w.borrow(), output[0]);
    assert_eq!(*alu.x.borrow(), output[1]);
    assert_eq!(*alu.y.borrow(), output[2]);
    assert_eq!(*alu.z.borrow(), output[3]);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(24);

    let part_1_answer = 0;
    assert_eq!(part_1_answer, 1);
}
