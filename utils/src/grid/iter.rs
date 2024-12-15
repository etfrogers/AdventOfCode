use super::pos::{Coord, CoordType};
use super::{direction::DIAGONAL_MOVES, direction::ORTHOGONAL_MOVES, Pos};
use super::{Grid, GridTrait};

#[derive(Debug, Clone, Copy)]
pub struct Invert(pub bool);

#[derive(Debug, Clone, Copy)]
pub struct ColumnMajor(pub bool);

impl<E> IntoIterator for Grid<E>
where
    E: Copy,
{
    type IntoIter = GridIntoIterator<E>;
    type Item = (Coord, E);

    fn into_iter(self) -> Self::IntoIter {
        GridIntoIterator::new(self, Invert(false), ColumnMajor(false))
    }
}

impl<'a, E> IntoIterator for &'a Grid<E>
where
    E: Copy,
{
    type IntoIter = GridIterator<'a, E>;
    type Item = (Coord, &'a E);

    fn into_iter(self) -> Self::IntoIter {
        self.iter()
    }
}

impl<'a, E> Grid<E> {
    pub fn iter_ordered(&'a self, invert: Invert, col_major: ColumnMajor) -> GridIterator<'a, E> {
        GridIterator::new(self, invert, col_major)
    }

    pub fn values(&'a self) -> GridValueIterator<'a, E> {
        GridValueIterator::new(self, Invert(false), ColumnMajor(false))
    }

    pub fn values_ordered(
        &'a self,
        invert: Invert,
        col_major: ColumnMajor,
    ) -> GridValueIterator<'a, E> {
        GridValueIterator::new(self, invert, col_major)
    }

    pub fn row_iter(&'a self) -> RowIterator<'a, E> {
        RowIterator::new(self)
    }

    pub fn col_iter(&'a self) -> ColumnIterator<'a, E> {
        ColumnIterator::new(self)
    }

    pub fn coords(&self) -> IndIterator {
        IndIterator::new(self, Invert(false), ColumnMajor(false))
    }

    pub fn neighbours(&self, coord: &Coord, include_diagonals: bool) -> NeighbourIterator<E> {
        NeighbourIterator::new(self, *coord, include_diagonals)
    }

    pub fn neighbour_coords(
        &self,
        coord: &Coord,
        include_diagonals: bool,
    ) -> NeighbourCoordIterator {
        NeighbourCoordIterator::new(self, *coord, include_diagonals)
    }
}

impl<E: Copy> Grid<E> {
    pub fn into_values(self) -> GridValueIntoIterator<E> {
        GridValueIntoIterator::new(self, Invert(false), ColumnMajor(false))
    }

    pub fn into_iter_ordered(self, invert: Invert, col_major: ColumnMajor) -> GridIntoIterator<E> {
        GridIntoIterator::new(self, invert, col_major)
    }
}

pub struct IndIterator {
    current_x: CoordType,
    current_y: CoordType,
    n_rows: usize,
    n_cols: usize,
    invert: Invert,
    exhausted: bool,
    col_major: ColumnMajor,
}

impl IndIterator {
    fn new<E>(g: &Grid<E>, invert: Invert, col_major: ColumnMajor) -> Self {
        let n_rows = g.n_rows();
        let n_cols = g.n_cols();
        let (current_x, current_y) = if invert.0 {
            (n_rows - 1, n_cols - 1)
        } else {
            (0, 0)
        };
        Self {
            current_x,
            current_y,
            n_rows,
            n_cols,
            invert,
            col_major,
            exhausted: false,
        }
    }

    fn reset_x(&mut self) {
        self.current_x = if self.invert.0 { self.n_cols - 1 } else { 0 };
    }

    fn reset_y(&mut self) {
        self.current_y = if self.invert.0 { self.n_rows - 1 } else { 0 };
    }
}

impl Iterator for IndIterator {
    type Item = Coord;

    fn next(&mut self) -> Option<Self::Item> {
        if self.exhausted {
            return None;
        }

        let step = if self.invert.0 { -1 } else { 1 };

        let inds = (self.current_x, self.current_y);
        if self.col_major.0 {
            let new_y = self.current_y.checked_add_signed(step);
            if new_y == Some(self.n_rows) || new_y.is_none() {
                self.reset_y();
                let new_x = self.current_x.checked_add_signed(step);
                if new_x == Some(self.n_cols) || new_x.is_none() {
                    self.exhausted = true;
                } else {
                    self.current_x = new_x.unwrap();
                }
            } else {
                self.current_y = new_y.unwrap();
            }
        } else {
            let new_x = self.current_x.checked_add_signed(step);
            if new_x == Some(self.n_cols) || new_x.is_none() {
                self.reset_x();
                let new_y = self.current_y.checked_add_signed(step);
                if new_y == Some(self.n_rows) || new_y.is_none() {
                    self.exhausted = true;
                } else {
                    self.current_y = new_y.unwrap();
                }
            } else {
                self.current_x = new_x.unwrap();
            }
        }
        Some(Coord::new(inds.0, inds.1))
    }
}

macro_rules! make_iterator {
    ($name:ident, $ret_type:ty, $next:expr) => {
        pub struct $name<'a, E> {
            ind_iter: IndIterator,
            grid: &'a Grid<E>,
        }

        impl<'a, E> $name<'a, E> {
            pub(super) fn new(grid: &'a Grid<E>, invert: Invert, col_major: ColumnMajor) -> Self {
                Self {
                    ind_iter: IndIterator::new(grid, invert, col_major),
                    grid,
                }
            }
        }

        impl<'a, E> Iterator for $name<'a, E> {
            type Item = $ret_type;

            fn next(&mut self) -> Option<Self::Item> {
                $next(self)
            }
        }
    };
    //------------- INTO ITER -------------
    ($name:ident, $ret_type:ty, $next:expr, into) => {
        pub struct $name<E: Copy> {
            ind_iter: IndIterator,
            grid: Grid<E>,
        }

        impl<E: Copy> $name<E> {
            fn new(grid: Grid<E>, invert: Invert, col_major: ColumnMajor) -> Self {
                Self {
                    ind_iter: IndIterator::new(&grid, invert, col_major),
                    grid,
                }
            }
        }

        impl<E: Copy> Iterator for $name<E> {
            type Item = $ret_type;

            fn next(&mut self) -> Option<Self::Item> {
                $next(self)
            }
        }
    };
}

make_iterator!(GridIterator, (Coord, &'a E), |me: &mut GridIterator<
    'a,
    E,
>| {
    let c = me.ind_iter.next()?;
    let item = &me.grid[c];
    Some((c, item))
});

make_iterator!(GridValueIterator, &'a E, |me: &mut GridValueIterator<
    'a,
    E,
>| {
    let c = me.ind_iter.next()?;
    let item = &me.grid[c];
    Some(item)
});

make_iterator!(
    GridIntoIterator,
    (Coord, E),
    |me: &mut GridIntoIterator<E>| {
        let c = me.ind_iter.next()?;
        let item = me.grid[c];
        Some((c, item))
    },
    into
);

make_iterator!(
    GridValueIntoIterator,
    E,
    |me: &mut GridValueIntoIterator<E>| {
        let c = me.ind_iter.next()?;
        let item = me.grid[c];
        Some(item)
    },
    into
);

pub struct RowIterator<'a, E> {
    grid: &'a Grid<E>,
    current_row: usize,
}

impl<'a, E> RowIterator<'a, E> {
    fn new(grid: &'a Grid<E>) -> Self {
        RowIterator {
            grid,
            current_row: 0,
        }
    }
}

impl<'a, E> Iterator for RowIterator<'a, E> {
    type Item = &'a Vec<E>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current_row == self.grid.n_rows() {
            return None;
        }
        let row = self.current_row;
        self.current_row += 1;
        Some(self.grid.get_row(row))
    }
}

pub struct ColumnIterator<'a, E> {
    grid: &'a Grid<E>,
    current_col: usize,
}

impl<'a, E> ColumnIterator<'a, E> {
    fn new(grid: &'a Grid<E>) -> Self {
        ColumnIterator {
            grid,
            current_col: 0,
        }
    }
}

impl<'a, E> Iterator for ColumnIterator<'a, E> {
    type Item = Vec<&'a E>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current_col == self.grid.n_cols() {
            return None;
        }
        let col = self.current_col;
        self.current_col += 1;
        Some(self.grid.get_col(col))
    }
}

pub struct NeighbourCoordIterator {
    current_ind: usize,
    positions: Vec<Pos>,
    coord: Coord,
    n_rows: usize,
    n_cols: usize,
}

impl NeighbourCoordIterator {
    fn new<E>(grid: &Grid<E>, coord: Coord, include_diagonals: bool) -> Self {
        let mut positions: Vec<_> = ORTHOGONAL_MOVES.values().copied().collect();
        if include_diagonals {
            positions.append(&mut DIAGONAL_MOVES.values().copied().collect());
        }
        Self {
            current_ind: 0,
            coord,
            positions,
            n_cols: grid.n_cols(),
            n_rows: grid.n_rows(),
        }
    }
}

impl Iterator for NeighbourCoordIterator {
    type Item = Coord;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current_ind == self.positions.len() {
            return None;
        }
        let p = TryInto::<Pos>::try_into(self.coord).unwrap() + self.positions[self.current_ind];
        self.current_ind += 1;
        // conversion to Coord deals with possible negative values - will return none
        if let Ok(coord) = Coord::try_from(p) {
            if coord.x() < self.n_cols && coord.y() < self.n_rows {
                Some(coord)
            } else {
                self.next()
            }
        } else {
            self.next()
        }
    }
}

pub struct NeighbourIterator<'a, E> {
    n: NeighbourCoordIterator,
    grid: &'a Grid<E>,
}

impl<'a, E> NeighbourIterator<'a, E> {
    fn new(grid: &'a Grid<E>, coord: Coord, include_diagonals: bool) -> Self {
        NeighbourIterator {
            n: NeighbourCoordIterator::new(grid, coord, include_diagonals),
            grid,
        }
    }
}

impl<'a, E> Iterator for NeighbourIterator<'a, E> {
    type Item = &'a E;

    fn next(&mut self) -> Option<Self::Item> {
        Some(&self.grid[self.n.next()?])
    }
}
