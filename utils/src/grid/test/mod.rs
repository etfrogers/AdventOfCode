use rstest::rstest;
use std::slice::SliceIndex;

use super::{
    iter::{ColumnMajor, Invert},
    pos::Coord,
    Grid,
};

#[rstest]
#[case(Invert(false), ColumnMajor(false), "ABCD", vec![(0,0), (1,0),(0,1), (1,1)])]
#[case(Invert(true), ColumnMajor(false), "DCBA", vec![(1,1), (0,1),(1,0), (0,0)])]
#[case(Invert(false), ColumnMajor(true), "ACBD", vec![(0,0), (0,1),(1,0), (1,1)])]
#[case(Invert(true), ColumnMajor(true), "DBCA", vec![(1,1), (1,0),(0,1), (0,0)])]
fn test_iterator(
    #[case] invert: Invert,
    #[case] col_major: ColumnMajor,
    #[case] expected_str: &str,
    #[case] expected_pos: Vec<(usize, usize)>,
) {
    let grid = Grid::new_from_string_slices(vec!["AB", "CD"]);
    let vec_chars = grid.values_ordered(invert, col_major).collect::<Vec<_>>();
    let actual: String = vec_chars.into_iter().collect();
    assert_eq!(expected_str, actual);

    let expected_pos: Vec<_> = expected_pos.iter().map(|t| Coord::from(*t)).collect();
    for (i, (p, v)) in grid.iter_ordered(invert, col_major).enumerate() {
        assert_eq!(p, expected_pos[i]);
        assert_eq!(*v, expected_str.chars().nth(i).unwrap());
    }

    for (i, (p, v)) in grid.into_iter_ordered(invert, col_major).enumerate() {
        assert_eq!(p, expected_pos[i]);
        assert_eq!(v, expected_str.chars().nth(i).unwrap());
    }
}

#[rstest]
#[case((.., 0..=0), "ABC")]
#[case((.., 1..=1), "DEF")]
#[case((.., 0..=1), "ABCDEF")]
#[case((.., 0..3), "ABCDEFGHI")]
#[case((0..=0, ..), "ADG")]
#[case((.., ..), "ABCDEFGHI")]
#[case((0..=1, ..2), "ABDE")]
fn test_slice<R1, R2>(#[case] index: (R1, R2), #[case] expected: &str)
where
    R1: SliceIndex<[char], Output = [char]> + Clone,
    R2: SliceIndex<[Vec<char>], Output = [Vec<char>]> + Clone,
{
    let grid = Grid::new_from_string_slices(vec!["ABC", "DEF", "GHI"]);
    let actual: String = grid
        .slice(index)
        .iter()
        .map(|v| v.iter().collect::<String>())
        .collect();
    assert_eq!(actual, expected)
}

#[rstest]
fn test_slice_round_trip() {
    let grid = Grid::new_from_string_slices(vec!["ABC", "DEF", "GHI"]);
    let actual: Grid<char> = grid.slice((.., ..)).into();
    assert_eq!(actual, grid)
}

#[rstest]
fn test_iter_mut() {
    let mut grid = Grid::from(vec![vec![0, 1, 2], vec![3, 4, 5], vec![6, 7, 8]]);
    for (p, v) in grid.iter_mut() {
        if *v >= 4 || p.x() == 2 {
            *v += 1
        }
    }
    assert_eq!(
        grid,
        Grid::from(vec![vec![0, 1, 3], vec![3, 5, 6], vec![7, 8, 9]])
    )
}

mod test_sparse;
