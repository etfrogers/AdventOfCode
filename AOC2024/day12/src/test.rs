use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_regions(input: Vec<String>) {
    let garden = Garden::new(input);
    let regions = garden.regions();
    assert_eq!(regions.len(), 11);
    let exp_list = vec![
        ('R', 12, 18, 216, 10),
        ('I', 4, 8, 32, 4),
        ('C', 14, 28, 392, 22),
        ('F', 10, 18, 180, 12),
        ('V', 13, 20, 260, 10),
        ('J', 11, 20, 220, 12),
        ('C', 1, 4, 4, 4),
        ('E', 13, 18, 234, 8),
        ('I', 14, 22, 308, 16),
        ('M', 5, 12, 60, 6),
        ('S', 3, 8, 24, 6),
    ];
    for (region, exp) in regions.iter().zip(exp_list) {
        // println!(
        //     "{}:, {} * {} = {} ... {}",
        //     region.label,
        //     region.area(),
        //     region.perimeter(),
        //     region.cost(false),
        //     region.n_sides()
        // );
        assert_eq!(region.label, exp.0);
        assert_eq!(region.area(), exp.1);
        assert_eq!(region.perimeter(), exp.2);
        assert_eq!(region.cost(false), exp.3);
        assert_eq!(region.n_sides(), exp.4);
    }
}

#[rstest]
fn test_small() {
    let input = utils::string_input_lines(
        "AAAA
BBCD
BBCC
EEEC",
    );
    let garden = Garden::new(input);
    let regions = garden.regions();
    assert_eq!(regions.len(), 5);
    // println!("{:?}", regions);
    let exp = [16, 16, 32, 4, 12];
    for (r, n) in regions.iter().zip(exp) {
        // println!("{}: {}", r.label, n);
        assert_eq!(r.cost(true), n);
    }
    assert_eq!(garden.total_fencing_cost(true), 80)
}

#[rstest]
fn test_xo() {
    let input = utils::string_input_lines(
        "OOOOO
OXOXO
OOOOO
OXOXO
OOOOO",
    );
    let garden = Garden::new(input);
    let regions = garden.regions();
    assert_eq!(regions.len(), 5);
    assert_eq!(garden.total_fencing_cost(true), 436)
}

#[rstest]
fn test_e() {
    let input = utils::string_input_lines(
        "EEEEE
EXXXX
EEEEE
EXXXX
EEEEE",
    );
    let garden = Garden::new(input);
    let regions = garden.regions();
    assert_eq!(regions.len(), 3);
    assert_eq!(regions[0].area(), 17);
    assert_eq!(garden.find_enclosures(&regions), vec![Vec::new(); 3]);
    assert_eq!(regions[0].n_sides(), 12);
    assert_eq!(garden.total_fencing_cost(true), 236)
}

#[rstest]
fn test_ab() {
    let input = utils::string_input_lines(
        "AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA",
    );
    let garden = Garden::new(input);
    let regions = garden.regions();
    assert_eq!(regions.len(), 3);
    assert_eq!(
        garden.find_enclosures(&regions),
        vec![vec![1, 2], Vec::new(), Vec::new()]
    );
    assert_eq!(regions[0].area(), 36 - 8);
    assert_eq!(regions[0].n_sides(), 12);
    assert_eq!(garden.total_fencing_cost(true), 368)
}

#[rstest]
fn test_enclosures() {
    let input = utils::string_input_lines(
        "AAAA
BBCD
BBCC
EEEC",
    );
    let garden = Garden::new(input);
    let regions = garden.regions();

    assert_eq!(garden.find_enclosures(&regions), vec![Vec::new(); 5])
}

#[rstest]
fn test_reddit_1() {
    let input = utils::string_input_lines(
        "AAAAAAAA
AACBBDDA
AACBBAAA
ABBAAAAA
ABBADDDA
AAAADADA
AAAAAAAA",
    );
    let garden = Garden::new(input);
    assert_eq!(garden.total_fencing_cost(true), 946)
}

#[rstest]
fn test_reddit_2() {
    let input = utils::string_input_lines(
        "CCAAA
CCAAA
AABBA
AAAAA",
    );
    let garden = Garden::new(input);
    for region in garden.regions() {
        println!(
            "{}:, {} * {} = {} ... {} * {} = {}",
            region.label,
            region.area(),
            region.perimeter(),
            region.cost(false),
            region.area(),
            region.n_sides(),
            region.cost(true),
        );
    }
    println!("{:?}", garden.find_enclosures(&garden.regions()));
    assert_eq!(garden.total_fencing_cost(true), 164)
}

#[rstest]
fn test_cost(input: Vec<String>) {
    let garden = Garden::new(input);
    assert_eq!(garden.total_fencing_cost(false), 1930)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(12);
    let garden = Garden::new(input);
    let part_1_answer = garden.total_fencing_cost(false);
    assert_eq!(part_1_answer, 1550156);
}
