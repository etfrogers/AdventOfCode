use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<";

const TEST_2: &str = "##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_build(input: Vec<String>) {
    let exp = "########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########
";
    let (wh, _) = build_warehouse(input, false);
    assert_eq!(wh.map.to_string(), exp);
}

#[rstest]
fn test_step(input: Vec<String>) {
    let (mut wh, moves) = build_warehouse(input, false);
    assert_eq!(
        wh.map.to_string(),
        "########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########
"
    );
    wh.move_robot(moves.0[0]);
    assert_eq!(
        wh.map.to_string(),
        "########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########
"
    );
    wh.move_robot(moves.0[1]);
    assert_eq!(
        wh.map.to_string(),
        "########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########
"
    );
}

#[rstest]
fn test_moves_1(input: Vec<String>) {
    let (mut wh, moves) = build_warehouse(input, false);
    wh.follow_instructions(moves);
    assert_eq!(
        wh.map.to_string(),
        "########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########
"
    )
}

#[rstest]
fn test_moves_2() {
    let (mut wh, moves) = build_warehouse(utils::string_input_lines(TEST_2), false);
    wh.follow_instructions(moves);
    assert_eq!(
        wh.map.to_string(),
        "##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########
"
    )
}

#[rstest]
#[case(
    "#######
#...O..
#......

",
    104
)]
#[case(TEST_1, 2028)]
#[case(TEST_2, 10092)]
fn test_gps(#[case] input: &str, #[case] exp: usize) {
    let (mut wh, moves) = build_warehouse(utils::string_input_lines(input), false);
    wh.follow_instructions(moves);
    assert_eq!(wh.gps(), exp);
}

#[rstest]
fn test_wide_build() {
    let (wh, _) = build_warehouse(utils::string_input_lines(TEST_2), true);
    assert_eq!(
        wh.map.to_string(),
        "####################
##....[]....[]..[]##
##............[]..##
##..[][]....[]..[]##
##....[]@.....[]..##
##[]##....[]......##
##[]....[]....[]..##
##..[][]..[]..[][]##
##........[]......##
####################
"
    );
}

#[test]
fn test_part1() {
    let input = utils::input_lines(15);
    let (mut wh, moves) = build_warehouse(input, false);
    wh.follow_instructions(moves);
    let part_1_answer = wh.gps();
    assert_eq!(part_1_answer, 1414416);
}
