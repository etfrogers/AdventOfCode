use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
#[case(0, Some((80, 40)), Some(280))]
#[case(1, None, None)]
#[case(2, Some((38, 86)), Some(200))]
#[case(3, None, None)]

fn test_costs(
    input: Vec<String>,
    #[case] i: usize,
    #[case] exp_p: Option<(u64, u64)>,
    #[case] exp_cost: Option<u64>,
) {
    let machines = ClawMachine::build_list(input);
    // assert!(machines[0].check(80, 40));
    let p = machines[i].n_presses();
    // println!("{:?}", p);
    assert_eq!(exp_p, p);
    if let Some(p) = p {
        assert!(machines[i].check(p.0, p.1));
    }
    assert_eq!(machines[i].cost_to_win(), exp_cost)
}

#[rstest]
fn test_total(input: Vec<String>) {
    let machines = ClawMachine::build_list(input);
    assert_eq!(ClawMachine::total_cost(&machines), 480)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(13);
    let machines = ClawMachine::build_list(input);
    let part_1_answer = ClawMachine::total_cost(&machines);
    assert_eq!(part_1_answer, 28138);
}
