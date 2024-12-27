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
fn test_cost(input: Vec<String>) {
    let garden = Garden::new(input);
    // let regions = garden.regions();
    assert_eq!(garden.total_fencing_cost(false), 1930)
}

#[test]
fn test_part1() {
    let input = utils::input_lines(12);
    let garden = Garden::new(input);
    let part_1_answer = garden.total_fencing_cost(false);
    assert_eq!(part_1_answer, 1550156);
}
