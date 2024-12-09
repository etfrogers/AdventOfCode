use rstest::rstest;

use crate::grid::{pos::Pos, sparse::SparseGrid};

#[rstest]
fn test_slice() {
    let mut grid = SparseGrid::new();
    grid[(0, 0)] = 1;
    grid[(10, 3)] = 2;
    grid[(1, -2)] = 3;
    grid[(-1, 4)] = 4;

    let mut iter = grid.slice((-5..=-1, ..));
    if let Some(actual) = iter.next() {
        assert_eq!(actual.0, (Pos::new(-1, 4)));
        assert_eq!(*actual.1, 4);
    } else {
        panic!("None found")
    };
    assert_eq!(iter.next(), None);

    let all: SparseGrid<_> = grid.slice((.., ..)).into();
    assert_eq!(all.len(), grid.len());

    let output: SparseGrid<_> = grid.slice((-2..=1, 0..)).into();
    assert_eq!(output.len(), 2);
    assert_eq!(output[Pos::new(0, 0)], 1);
    assert_eq!(output[Pos::new(-1, 4)], 4);

    let mut iter = grid.slice((-10..=-2, ..));
    assert_eq!(iter.next(), None);

    let output: SparseGrid<_> = grid.slice((.., ..)).into();
    assert_eq!(output, grid);
}
