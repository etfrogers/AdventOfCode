use std::{
    error::Error,
    fmt::{self, Display},
    ops::{Index, IndexMut},
};

use pos::Pos;

pub mod direction;
mod iter;
pub mod pos;
pub mod sparse;

type CoordType = usize;

struct Coord {
    x: CoordType,
    y: CoordType,
}
impl Coord {
    fn from(p: &Pos) -> Option<Self> {
        Some(Self {
            x: p.x().try_into().ok()?,
            y: p.y().try_into().ok()?,
        })
    }
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
    pub fn is_inside(&self, x: CoordType, y: CoordType) -> bool {
        x < self.n_cols() && y < self.n_rows()
    }

    pub fn inside_c(&self, coord: &Pos) -> bool {
        if let Some(c) = Coord::from(&coord) {
            self.is_inside(c.x, c.y)
        } else {
            false
        }
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

    pub fn map<F, T>(&self, fun: F) -> Grid<T>
    where
        F: Fn(&E) -> T,
        T: Clone + Default,
    {
        let mut new = Grid::full(self.n_cols(), self.n_rows(), T::default());
        let ind_it = self.coord_iter(false, false);
        for c in ind_it {
            let elem = &self[c];
            new[c] = fun(elem);
        }
        new
    }
}

impl<E> Index<Pos> for Grid<E> {
    type Output = E;

    fn index(&self, index: Pos) -> &Self::Output {
        let coord = Coord::from(&index).expect("Coord out of bounds - probably negative");
        &self.data[coord.y][coord.x]
    }
}

impl<E> IndexMut<Pos> for Grid<E> {
    fn index_mut(&mut self, index: Pos) -> &mut Self::Output {
        let coord = Coord::from(&index).expect("Coord out of bounds - probably negative");
        &mut self.data[coord.y][coord.x]
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
        let c = self.find_c(val)?;
        Some((c.x().try_into().unwrap(), c.y().try_into().unwrap()))
    }

    pub fn find_c(&self, val: E) -> Option<Pos> {
        for c in self.coord_iter(false, false) {
            if self[c] == val {
                return Some(c);
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
