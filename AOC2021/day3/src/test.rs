use super::*;

const TEST_1: &str = "00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010";

#[test]
fn test_power_consumption(){
    let input = utils::string_input_lines(TEST_1);
    let report = Report::build(input);
    let power = report.power_consumption();
    assert_eq!(power, 198)
}

#[test]
fn test_gamma_epsilon(){
    let input = utils::string_input_lines(TEST_1);
    let report = Report::build(input);
    assert_eq!(report.gamma_rate, 22);
    assert_eq!(report.epsilon_rate, 9);
}

#[test]
fn test_oxgen_co2(){
    let input = utils::string_input_lines(TEST_1);
    let report = Report::build(input);
    assert_eq!(report.oxygen_rating, 23);
    assert_eq!(report.co2_rating, 10);
}


#[test]
fn test_life_support_rating(){
    let input = utils::string_input_lines(TEST_1);
    let report = Report::build(input);
    assert_eq!(report.life_support_rating(), 230);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(3);
    let report = Report::build(input);
    let part1 = report.power_consumption();
    assert_eq!(part1, 4160394);
}

#[test]
fn test_part2() {
    let input = utils::input_lines(3);
    let report = Report::build(input);
    let part2 = report.life_support_rating();
    assert_eq!(part2, 4125600);
}
