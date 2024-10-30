use std::{
    collections::HashMap,
    error::Error,
    fmt::{self, Display},
    num::TryFromIntError,
    ops::{Deref, Index, IndexMut},
    slice::SliceIndex,
    str::FromStr,
};

use super::{
    pos::{Coord, CoordType, Pos},
    sparse::SparseGrid,
    GridBounds, GridTrait,
};

#[derive(Clone, Debug, PartialEq)]
pub struct Grid<E> {
    data: Vec<Vec<E>>,
}

impl<'a, E: 'a + Clone> GridTrait<'a, E> for Grid<E> {
    type SliceType = GridSlice<'a, E> where E: 'a;

    type CoordType = usize;

    fn is_inside(&self, coord: &Pos) -> bool {
        if let Ok(c) = Coord::try_from(*coord) {
            c.x() < self.n_cols() && c.y() < self.n_rows()
        } else {
            false
        }
    }

    fn bounds(&self) -> GridBounds<Self::CoordType> {
        GridBounds {
            min_x: 0,
            min_y: 0,
            max_x: self.n_cols(),
            max_y: self.n_rows(),
        }
    }

    fn size(&self) -> (CoordType, CoordType) {
        (self.n_cols(), self.n_rows())
    }
    fn n_elem(&self) -> CoordType {
        self.n_cols() * self.n_rows()
    }
    #[allow(refining_impl_trait)]
    fn map<'b, F, T: 'b>(&'b self, fun: F) -> Grid<T>
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

    fn apply(&mut self, fun: impl Fn(&E) -> E) {
        let iter = self.coord_iter(false, false);
        for pos in iter {
            self.data[pos.y()][pos.x()] = fun(&self[pos])
        }
    }
}

impl<E: Clone> Grid<E> {
    pub fn slice<'b, R1, R2>(&'b self, index: (R1, R2)) -> <Grid<E> as GridTrait<E>>::SliceType
    where
        R1: 'b + SliceIndex<[E], Output = [E]> + Clone,
        R2: 'b + SliceIndex<[Vec<E>], Output = [Vec<E>]> + Clone,
    {
        let data: Vec<&[E]> = self.data[index.1]
            .iter()
            .enumerate()
            .map(|(_, v)| &v[index.0.clone()])
            .collect();
        GridSlice(data)
    }
}

impl<E> Grid<E> {
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

    fn check_lengths(&self) {
        let base_len = self.data[0].len();
        for row in self.data.iter() {
            if row.len() != base_len {
                panic!("All lines in a grid must have the same length")
            }
        }
    }
}

impl<E: Clone> From<Vec<Vec<E>>> for Grid<E> {
    fn from(value: Vec<Vec<E>>) -> Self {
        let g = Grid { data: value };
        g.check_lengths();
        g
    }
}

impl<E> Index<Pos> for Grid<E> {
    type Output = E;

    fn index(&self, index: Pos) -> &Self::Output {
        let coord = Coord::try_from(index).expect("Coord out of bounds - probably negative");
        &self.data[coord.y()][coord.x()]
    }
}

impl<E> IndexMut<Pos> for Grid<E> {
    fn index_mut(&mut self, index: Pos) -> &mut Self::Output {
        let coord = Coord::try_from(index).expect("Coord out of bounds - probably negative");
        &mut self.data[coord.y()][coord.x()]
    }
}

impl<E> Index<Coord> for Grid<E> {
    type Output = E;

    fn index(&self, index: Coord) -> &Self::Output {
        &self.data[index.y()][index.x()]
    }
}

impl<E> IndexMut<Coord> for Grid<E> {
    fn index_mut(&mut self, index: Coord) -> &mut Self::Output {
        &mut self.data[index.y()][index.x()]
    }
}

impl<E> Index<(usize, usize)> for Grid<E> {
    type Output = E;

    fn index(&self, index: (usize, usize)) -> &Self::Output {
        &self.data[index.1][index.0]
    }
}

impl<E> IndexMut<(usize, usize)> for Grid<E> {
    fn index_mut(&mut self, index: (usize, usize)) -> &mut Self::Output {
        &mut self.data[index.1][index.0]
    }
}

impl FromStr for Grid<char> {
    type Err = fmt::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self::new_from_strings(
            s.lines().map(String::from).collect(),
        ))
    }
}

impl Grid<char> {
    pub fn new_from_strings(lines: Vec<String>) -> Self {
        let mut data = Vec::with_capacity(lines.len());
        for line in lines {
            data.push(line.chars().collect())
        }
        data.into()
    }

    pub fn new_from_string_slices(lines: Vec<&str>) -> Self {
        Grid::new_from_strings(lines.into_iter().map(String::from).collect())
    }
}

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

impl<E> TryFrom<SparseGrid<E>> for Grid<E>
where
    E: Default + Copy,
{
    type Error = TryFromIntError;

    fn try_from(value: SparseGrid<E>) -> Result<Self, Self::Error> {
        let GridBounds {
            min_x,
            max_x: _,
            min_y,
            max_y: _,
        } = value.bounds();
        let shift = Pos::new(min_x, min_y);

        let grid_data: HashMap<Coord, E> = value
            .iter()
            .map(|(pos, v)| -> Result<(Pos<usize>, E), TryFromIntError> {
                let pos32: Pos<i32> = (*pos).try_into()?;
                let shifted_pos: Coord = (pos32 - shift).try_into()?;
                Ok((shifted_pos, *v))
            })
            .collect::<Result<HashMap<_, _>, TryFromIntError>>()?;

        let def = value.default().unwrap_or(E::default());
        let (x, y) = value.size();
        let mut new_grid = Self::full(x, y, def);
        for (pos, v) in grid_data.iter() {
            new_grid[*pos] = *v;
        }
        Ok(new_grid)
    }
}

impl<E: PartialEq> Grid<E> {
    // Returns x and y coords of first occurence of the input val
    // If the value is not found, None
    pub fn find(&self, val: E) -> Option<(CoordType, CoordType)> {
        let c = self.find_c(val)?;
        Some((c.x(), c.y()))
    }

    pub fn find_c(&self, val: E) -> Option<Coord> {
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

// ############################

pub struct GridSlice<'a, E>(Vec<&'a [E]>);

impl<'a, E: Clone> From<GridSlice<'a, E>> for Grid<E> {
    fn from(value: GridSlice<'a, E>) -> Self {
        value
            .0
            .into_iter()
            .map(|row| Vec::from(row))
            .collect::<Vec<_>>()
            .into()
    }
}

impl<'a, E> Deref for GridSlice<'a, E> {
    type Target = Vec<&'a [E]>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

//######################

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
