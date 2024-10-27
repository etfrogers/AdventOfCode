use rstest::rstest;
use std::slice::SliceIndex;

use super::Grid;

#[rstest]
#[case(false, false, "ABCD")]
// 	{true, false, "DCBA"},
// 	{false, true, "ACBD"},
// 	{true, true, "DBCA"},
fn test_iterator(#[case] _invert: bool, #[case] _col_major: bool, #[case] expected: &str) {
    let grid = Grid::new_from_string_slices(vec!["AB", "CD"]);
    let vec_chars = grid.iter().collect::<Vec<_>>();
    let actual: String = vec_chars.into_iter().collect();
    assert_eq!(expected, actual);
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

mod test_sparse;
