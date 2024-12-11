use super::pos::Coord;
use super::pos::CoordType;
use super::pos::DIAGONAL_MOVES;
use super::Grid;
use super::{pos::ORTHOGONAL_MOVES, Pos};

pub struct Invert(pub bool);
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
    pub fn iter(&'a self) -> GridIterator<'a, E> {
        // two args: invert, and colMajor, both bool, default false
        GridIterator::new(&self, Invert(false), ColumnMajor(false))
    }

    pub fn values(&'a self) -> GridValueIterator<'a, E> {
        // two args: invert, and colMajor, both bool, default false
        GridValueIterator::new(&self, Invert(false), ColumnMajor(false))
    }

    pub fn values_ordered(
        &'a self,
        invert: Invert,
        col_major: ColumnMajor,
    ) -> GridValueIterator<'a, E> {
        // two args: invert, and colMajor, both bool, default false
        GridValueIterator::new(&self, invert, col_major)
    }

    pub fn iter_ordered(&'a self, invert: Invert, col_major: ColumnMajor) -> GridIterator<'a, E> {
        // two args: invert, and colMajor, both bool, default false
        GridIterator::new(&self, invert, col_major)
    }

    pub fn row_iter(&'a self) -> RowIterator<'a, E> {
        RowIterator::new(&self)
    }

    pub fn col_iter(&'a self) -> ColumnIterator<'a, E> {
        ColumnIterator::new(&self)
    }

    pub fn coords(&self) -> IndIterator {
        return IndIterator::new(self, Invert(false), ColumnMajor(false));
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
        // two args: invert, and colMajor, both bool, default false
        GridValueIntoIterator::new(self, Invert(false), ColumnMajor(false))
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

pub struct GridIterator<'a, E> {
    ind_iter: IndIterator,
    grid: &'a Grid<E>,
}

impl<'a, E> GridIterator<'a, E> {
    fn new(grid: &'a Grid<E>, invert: Invert, col_major: ColumnMajor) -> Self {
        Self {
            ind_iter: IndIterator::new(grid, invert, col_major),
            grid,
        }
    }
}

impl<'a, E> Iterator for GridIterator<'a, E> {
    type Item = (Coord, &'a E);

    fn next(&mut self) -> Option<Self::Item> {
        let c = self.ind_iter.next()?;
        let item = &self.grid[c];
        Some((c, item))
    }
}

pub struct GridValueIterator<'a, E> {
    ind_iter: IndIterator,
    grid: &'a Grid<E>,
}

impl<'a, E> GridValueIterator<'a, E> {
    fn new(g: &'a Grid<E>, invert: Invert, col_major: ColumnMajor) -> Self {
        Self {
            ind_iter: IndIterator::new(g, invert, col_major),
            grid: g,
        }
    }
}

impl<'a, E> Iterator for GridValueIterator<'a, E> {
    type Item = &'a E;

    fn next(&mut self) -> Option<Self::Item> {
        let c = self.ind_iter.next()?;
        let item = &self.grid[c];
        Some(item)
    }
}

pub struct GridIntoIterator<E>
where
    E: Copy,
{
    ind_iter: IndIterator,
    grid: Grid<E>,
}

impl<'a, E> GridIntoIterator<E>
where
    E: Copy,
{
    fn new(g: Grid<E>, invert: Invert, col_major: ColumnMajor) -> Self {
        Self {
            ind_iter: IndIterator::new(&g, invert, col_major),
            grid: g,
        }
    }
}

impl<'a, E> Iterator for GridIntoIterator<E>
where
    E: Copy,
{
    type Item = (Coord, E);

    fn next(&mut self) -> Option<Self::Item> {
        let c = self.ind_iter.next()?;
        let item = self.grid[c];
        Some((c, item))
    }
}

pub struct GridValueIntoIterator<E>
where
    E: Copy,
{
    ind_iter: IndIterator,
    grid: Grid<E>,
}

impl<'a, E> GridValueIntoIterator<E>
where
    E: Copy,
{
    fn new(g: Grid<E>, invert: Invert, col_major: ColumnMajor) -> Self {
        Self {
            ind_iter: IndIterator::new(&g, invert, col_major),
            grid: g,
        }
    }
}

impl<'a, E> Iterator for GridValueIntoIterator<E>
where
    E: Copy,
{
    type Item = E;

    fn next(&mut self) -> Option<Self::Item> {
        let c = self.ind_iter.next()?;
        let item = self.grid[c];
        Some(item)
    }
}

pub struct RowIterator<'a, E> {
    grid: &'a Grid<E>,
    current_row: usize,
}

impl<'a, E> RowIterator<'a, E> {
    fn new(grid: &'a Grid<E>) -> Self {
        return RowIterator {
            grid,
            current_row: 0,
        };
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
        return ColumnIterator {
            grid,
            current_col: 0,
        };
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
            positions.append(&mut DIAGONAL_MOVES.clone());
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
