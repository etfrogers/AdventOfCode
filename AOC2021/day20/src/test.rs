use super::*;
use rstest::{fixture, rstest};
use utils::string_input_lines;

const TEST_1: &str = "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_build(input: Vec<String>) {
    let (algo, img) = parse_input(input);
    assert_eq!(algo[0], Pixel::Dark);
    assert_eq!(algo[1], Pixel::Dark);
    assert_eq!(algo[2], Pixel::Light);
    assert_eq!(*algo.last().unwrap(), Pixel::Light);
    assert_eq!(*img.counter().get(&Pixel::Light).unwrap(), 10)
}

#[rstest]
fn test_1_enhance(input: Vec<String>) {
    let expected = Image::new_from_strings(&string_input_lines(
        ".##.##.
#..#.#.
##.#..#
####..#
.#..##.
..##..#
...#.#.",
    ));

    let (algo, mut img) = parse_input(input);
    let (ox, oy) = img.size();
    img.enhance(&algo);

    // Sanity check on inputs
    let (ex, ey) = expected.size();
    assert_eq!(ex, ox + 2);
    assert_eq!(ey, oy + 2);

    // Check on output size
    let (nx, ny) = img.size();
    assert_eq!(nx, ox + 2);
    assert_eq!(ny, oy + 2);

    // println!("{}", img);
    // println!("{}", expected);

    assert_eq!(img, expected)
}

#[rstest]
fn test_2_enhance(input: Vec<String>) {
    let (algo, mut img) = parse_input(input);
    img.enhance_n(&algo, 2);
    // println!("{img}");
    assert_eq!(img.counter()[&Pixel::Light], 35);
}

#[rstest]
fn test_50_enhance(input: Vec<String>) {
    let (algo, mut img) = parse_input(input);
    img.enhance_n(&algo, 50);
    // println!("{img}");
    assert_eq!(img.counter()[&Pixel::Light], 3351);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(20);
    let (algo, mut img) = parse_input(input);
    img.enhance_n(&algo, 2);
    let part_1_answer = img.counter()[&Pixel::Light];
    assert_eq!(part_1_answer, 5291);
}

#[test]
fn test_part2() {
    let input = utils::input_lines(20);
    let (algo, mut img) = parse_input(input);
    img.enhance_n(&algo, 50);
    let part_1_answer = img.counter()[&Pixel::Light];
    assert_eq!(part_1_answer, 16665);
}
