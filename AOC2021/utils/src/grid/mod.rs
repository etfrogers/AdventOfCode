use std::{
    error::Error,
    fmt::{self, Display},
};

use pos::Pos;

pub mod direction;
pub mod pos;
pub mod sparse;

type CoordType = usize;

pub trait Coord {
    fn xc(&self) -> CoordType;
    fn yc(&self) -> CoordType;
}

#[derive(Clone, Debug, PartialEq)]
pub struct Grid<E> {
    data: Vec<Vec<E>>,
}

#[derive(Debug)]
pub struct IndexError {
    msg: String,
}

impl Error for IndexError {}

impl fmt::Display for IndexError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Error indexing into grid: {}", self.msg)
    }
}

impl<'a, E> Grid<E> {
    pub fn get(&self, x: CoordType, y: CoordType) -> &E {
        &self.data[y][x]
    }

    pub fn get_c<C: Coord>(&self, coord: &C) -> &E {
        &self.data[coord.xc()][coord.yc()]
    }

    pub fn is_inside(&self, x: CoordType, y: CoordType) -> bool {
        x < self.n_cols() && y < self.n_rows()
    }

    pub fn inside_c(&self, c: &impl Coord) -> bool {
        self.is_inside(c.xc(), c.yc())
    }

    pub fn set(&mut self, x: CoordType, y: CoordType, val: E) {
        self.data[y][x] = val;
    }

    pub fn set_c(&mut self, c: &impl Coord, val: E) {
        self.data[c.yc()][c.xc()] = val;
    }

    // Can edit the returned values to set elements
    pub fn get_row(&self, y: CoordType) -> &Vec<E> {
        &self.data[y]
    }

    // CanNOT edit the returned values to set elements
    pub fn get_col(&self, x: CoordType) -> Vec<&E> {
        let mut col = Vec::with_capacity(self.data.len());
        for i in 0..self.data.len() {
            col.push(&self.data[i][x])
        }
        col
    }

    pub fn insert_row(&mut self, y: CoordType, data: Vec<E>) -> Result<(), IndexError> {
        if data.len() != self.n_cols() {
            return Err(IndexError {
                msg: format!(
                    "length of new data was {}. Existing row length is {}. These values must match",
                    data.len(),
                    self.n_rows()
                ),
            });
        }
        self.data.insert(y, data);
        Ok(())
    }

    pub fn insert_col(&mut self, x: CoordType, data: Vec<E>) -> Result<(), IndexError> {
        if data.len() != self.n_rows() {
            return Err(IndexError {
                msg: format!(
                    "length of new data was {}. Existing row length is {}. These values must match",
                    data.len(),
                    self.n_rows()
                ),
            });
        }
        for (row, new_element) in self.data.iter_mut().zip(data.into_iter()) {
            row.insert(x, new_element);
        }
        Ok(())
    }

    pub fn n_cols(&self) -> CoordType {
        self.data[0].len()
    }

    pub fn n_rows(&self) -> CoordType {
        self.data.len()
    }

    pub fn size(&self) -> (CoordType, CoordType) {
        (self.n_cols(), self.n_rows())
    }

    pub fn n_elem(&self) -> CoordType {
        self.n_cols() * self.n_rows()
    }

    fn check_lengths(&self) {
        let base_len = self.data[0].len();
        for row in self.data.iter() {
            if row.len() != base_len {
                panic!("All lines in a grid must have the same length")
            }
        }
    }

    pub fn new_from(input: Vec<Vec<E>>) -> Self {
        let g = Grid { data: input };
        g.check_lengths();
        g
    }

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

    pub fn map<F, T: Clone>(&self, fun: F) -> Grid<T>
    where
        F: Fn(&E) -> T,
    {
        let mut new = Grid::full(self.n_cols(), self.n_rows(), fun(self.get(0, 0)));
        let ind_it = self.ind_iter(false, false);
        for (x, y) in ind_it {
            let elem = self.get(x, y);
            new.set(x, y, fun(elem));
        }
        new
    }

    pub fn ind_iter(&self, invert: bool, col_major: bool) -> IndIterator<E> {
        return IndIterator::new(self, invert, col_major);
    }
}

pub struct IndIterator<'a, E> {
    current_x: CoordType,
    current_y: CoordType,
    grid: &'a Grid<E>,
    _invert: bool,
    _col_major: bool,
}

impl<'a, E> IndIterator<'a, E> {
    fn new(g: &'a Grid<E>, invert: bool, col_major: bool) -> Self {
        match (invert, col_major) {
            (false, false) => Self {
                current_x: 0,
                current_y: 0,
                grid: g,
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

impl<'a, E> Iterator for IndIterator<'a, E> {
    type Item = (CoordType, CoordType);

    fn next(&mut self) -> Option<Self::Item> {
        if self.current_y == self.grid.n_cols() {
            return None;
        }

        let inds = (self.current_x, self.current_y);
        self.current_x += 1;
        if self.current_x == self.grid.n_cols() {
            self.current_x = 0;
            self.current_y += 1;
        }
        Some(inds)
    }
}

pub struct GridIterator<'a, E> {
    ind_iter: IndIterator<'a, E>,
}

impl<'a, E> GridIterator<'a, E> {
    fn new(g: &'a Grid<E>, invert: bool, col_major: bool) -> Self {
        GridIterator {
            ind_iter: IndIterator::new(g, invert, col_major),
        }
    }
}

impl<'a, E> Iterator for GridIterator<'a, E> {
    type Item = &'a E;

    fn next(&mut self) -> Option<Self::Item> {
        let (x, y) = self.ind_iter.next()?;
        let item = self.ind_iter.grid.get(x, y);
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

impl Grid<char> {
    pub fn new_from_strings(lines: Vec<String>) -> Self {
        let mut data = Vec::with_capacity(lines.len());
        for line in lines {
            data.push(line.chars().collect())
        }
        Grid { data }
    }
}

/*
impl fmt::Display for Grid<char> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut string: String = String::with_capacity(self.n_elem());
        for row in self.data.iter() {
            string.push_str(&(String::from_iter(row) + "\n"));
        }
        string.trim();
        write!(f, "{}", string)
    }
}
    */

impl<E: Display> fmt::Display for Grid<E> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for row in &self.data {
            for item in row {
                write!(f, "{}", item)?;
            }
            write!(f, "\n")?;
        }
        Ok(())
    }
}

impl<E: PartialEq> Grid<E> {
    // Returns x and y coords of first occurence of the input val
    // If the value is not found, None
    pub fn find(&self, val: E) -> Option<(CoordType, CoordType)> {
        for (x, y) in self.ind_iter(false, false) {
            if *self.get(x, y) == val {
                return Some((x, y));
            }
        }
        None
    }

    pub fn find_c(&self, val: E) -> Option<Pos> {
        for (x, y) in self.ind_iter(false, false) {
            if *self.get(x, y) == val {
                return Some(pos::Pos::new(x.try_into().unwrap(), y.try_into().unwrap()));
            }
        }
        None
    }
}

impl<E: Clone> Grid<E> {
    pub fn full(x: CoordType, y: CoordType, content: E) -> Grid<E> {
        let mut data = Vec::with_capacity(y);
        for _ in 0..y {
            data.push(vec![content.clone(); x])
        }
        Grid { data }
    }
}
