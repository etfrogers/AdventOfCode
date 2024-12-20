use super::*;
use rstest::{fixture, rstest};
use utils::grid::GridFind;

const TEST_1: &str = "............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_parse(input: Vec<String>) {
    let ants = Antennas::new(input);
    assert_eq!(ants.0.find_all('0').collect::<Vec<_>>().len(), 4);
    assert_eq!(ants.0.find_all('A').collect::<Vec<_>>().len(), 3);
}

#[rstest]
fn test_antinodes(input: Vec<String>) {
    let ants = Antennas::new(input);
    let an = ants.find_antinodes();
    // println!("{:?}", ants);
    // println!("{:?}", an);
    assert_eq!(an.len(), 14)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(8);
    let ants = Antennas::new(input);
    let antinodes = ants.find_antinodes();
    let part_1_answer = antinodes.len();
    assert_eq!(part_1_answer, 252);
}
