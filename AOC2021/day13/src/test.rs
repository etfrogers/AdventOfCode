use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_build(input: Vec<String>) {
    let (coords, folds) = parse_input(input);
    assert_eq!(
        folds[0],
        Fold {
            orientation: Orientation::Y,
            coord: 7
        }
    );
    assert_eq!(
        folds[1],
        Fold {
            orientation: Orientation::X,
            coord: 5
        }
    );
    assert_eq!(coords[0].x(), 6);
    assert_eq!(coords[0].y(), 10);
    assert_eq!(coords.len(), 18);

    let expected = "...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
";
    let paper = Paper::build(&coords);
    let actual = paper.to_string();
    assert_eq!(actual, expected);
}

#[rstest]
fn test_fold(input: Vec<String>) {
    let (coords, folds) = parse_input(input);
    let mut paper = Paper::build(&coords);
    paper.fold(&folds[0]);
    let expected = "#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
";
    // ...........
    // ...........
    // ";
    let actual = paper.to_string();
    assert_eq!(actual, expected);
    assert_eq!(paper.n_dots(), 17);

    paper.fold(&folds[1]);
    let expected = "#####
#...#
#...#
#...#
#####
";
    // .....
    // ....."
    let actual = paper.to_string();
    assert_eq!(actual, expected);
    assert_eq!(paper.n_dots(), 16);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(13);
    let (coords, folds) = parse_input(input);
    let mut paper = Paper::build(&coords);
    paper.fold(&folds[0]);
    let part_1_answer = paper.n_dots();
    assert_eq!(part_1_answer, 684);
}
