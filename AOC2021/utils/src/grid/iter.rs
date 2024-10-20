use super::pos::DIAGONAL_MOVES;
use super::{pos::ORTHOGONAL_MOVES, CoordType, Pos};
use super::{Coord, Grid};

impl<'a, E> Grid<E> {
    pub fn iter(&'a self) -> GridIterator<'a, E> {
        // two args: invert, and colMajor, both bool, default false
        GridIterator::new(&self, false, false)
    }

    pub fn row_iter(&'a self) -> RowIterator<'a, E> {
        RowIterator::new(&self)
    }

    pub fn col_iter(&'a self) -> ColumnIterator<'a, E> {
        ColumnIterator::new(&self)
    }

    pub fn coord_iter(&self, invert: bool, col_major: bool) -> IndIterator {
        return IndIterator::new(self, invert, col_major);
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

pub struct IndIterator {
    current_x: CoordType,
    current_y: CoordType,
    n_rows: usize,
    n_cols: usize,
    _invert: bool,
    _col_major: bool,
}

impl IndIterator {
    fn new<E>(g: &Grid<E>, invert: bool, col_major: bool) -> Self {
        match (invert, col_major) {
            (false, false) => Self {
                current_x: 0,
                current_y: 0,
                n_rows: g.n_rows(),
                n_cols: g.n_cols(),
                _invert: false,
                _col_major: false,
            },
            _ => todo!("Not implemented"),
        }
    }
    /*
            case invert && !colMajor:
        {
            fn(yield fn(CoordType, CoordType) bool) {
                for y := range i.CountDown(self.n_rows()) {
                    for x := range i.CountDown(self.n_cols()) {
                        if !yield(x, y) {

                        }
                    }
                }
            }
        }
    case !invert && colMajor:
        {
            fn(yield fn(CoordType, CoordType) bool) {
                for x := range self.n_cols() {
                    for y := range self.n_rows() {
                        if !yield(x, y) {

                        }
                    }
                }
            }
        }
    case invert && colMajor:
        {
            fn(yield fn(CoordType, CoordType) bool) {
                for x := range i.CountDown(self.n_cols()) {
                    for y := range i.CountDown(self.n_rows()) {
                        if !yield(x, y) {

                        }
                    }
                }
            }
        }
    */
}

impl Iterator for IndIterator {
    type Item = Coord;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current_y == self.n_rows {
            return None;
        }

        let inds = (self.current_x, self.current_y);
        self.current_x += 1;
        if self.current_x == self.n_cols {
            self.current_x = 0;
            self.current_y += 1;
        }
        Some(Coord::new(inds.0, inds.1))
    }
}

pub struct GridIterator<'a, E> {
    ind_iter: IndIterator,
    grid: &'a Grid<E>,
}

impl<'a, E> GridIterator<'a, E> {
    fn new(g: &'a Grid<E>, invert: bool, col_major: bool) -> Self {
        GridIterator {
            ind_iter: IndIterator::new(g, invert, col_major),
            grid: g,
        }
    }
}

impl<'a, E> Iterator for GridIterator<'a, E> {
    type Item = &'a E;

    fn next(&mut self) -> Option<Self::Item> {
        let c = self.ind_iter.next()?;
        let item = &self.grid[c];
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
    type Item = Pos;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current_ind == self.positions.len() {
            return None;
        }
        let p = self.coord + self.positions[self.current_ind];
        self.current_ind += 1;
        // conversion to Coord deals with possible negative values - will return none
        if let Some(coord) = Coord::from(&p) {
            if coord.x < self.n_cols && coord.y < self.n_rows {
                Some(p)
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
