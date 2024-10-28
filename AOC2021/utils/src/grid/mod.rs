use std::{
    error::Error,
    fmt::{self, Display},
    ops::{Deref, Index, IndexMut},
    slice::SliceIndex,
    str::FromStr,
};

use num::PrimInt;
use pos::{Coord, CoordType, Pos};

pub mod coord;
pub mod direction;
mod iter;
pub mod pos;
pub mod sparse;

pub trait GridTrait<'a, E>: Index<Pos> + IndexMut<Pos> + From<Self::SliceType>
where
    Self: 'a,
{
    type SliceType;
    type CoordType: PrimInt;

    fn is_inside(&self, coord: &Pos) -> bool;
    fn size(&self) -> (CoordType, CoordType);
    fn n_elem(&self) -> CoordType;
    fn map<'b, F, T: 'b>(&'b self, fun: F) -> impl GridTrait<T>
    where
        F: Fn(&E) -> T,
        T: Clone + Default + Copy;
    fn apply(&mut self, fun: impl Fn(&E) -> E);
    // fn slice<'a, R1, R2>(&'a self, index: (R1, R2)) -> Self::SliceType<'a>
    // where
    //     R1: 'a + RangeBounds<Self::CoordType> + SliceIndex<[E], Output = [E]> + Clone,
    //     R2: 'a + RangeBounds<Self::CoordType> + SliceIndex<[E], Output = [E]> + Clone,
    //     E: Copy;
}

// pub trait SliceTrait<E> {
//     type GridType: GridTrait<E>;
//     fn to_grid(self) -> Self::GridType;
// }

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

impl<'a, E: 'a> GridTrait<'a, E> for Grid<E> {
    fn is_inside(&self, coord: &Pos) -> bool {
        if let Ok(c) = Coord::try_from(*coord) {
            c.x() < self.n_cols() && c.y() < self.n_rows()
        } else {
            false
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
    type CoordType = usize;
    type SliceType = GridSlice<'a, E> where E: 'a;
}

impl<E> Grid<E> {
    fn slice<'b, R1, R2>(&'b self, index: (R1, R2)) -> <Grid<E> as GridTrait<E>>::SliceType
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

impl<'a, E> Grid<E> {
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

    pub fn new_from(input: Vec<Vec<E>>) -> Self {
        let g = Grid { data: input };
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
        Grid::new_from(data)
    }

    pub fn new_from_string_slices(lines: Vec<&str>) -> Self {
        Grid::new_from_strings(lines.into_iter().map(String::from).collect())
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

pub struct GridSlice<'a, E>(Vec<&'a [E]>);

// impl<'a, E> SliceTrait<E> for GridSlice<'a, E> {
//     fn to_grid(self) -> Self::GridType {
//         todo!()
//     }

//     type GridType = Grid<E>;
// }

impl<'a, E> From<GridSlice<'a, E>> for Grid<E> {
    fn from(value: GridSlice<'a, E>) -> Self {
        todo!()
    }
}

impl<'a, E> Deref for GridSlice<'a, E> {
    type Target = Vec<&'a [E]>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

// impl<E> Grid<E> {
//     fn slice<'a, R1, R2>(&self, index: (R1, R2)) -> GridSlice<'a, E>
//     where
//         R1: 'a + RangeBounds<usize> + SliceIndex<[E], Output = [E]> + Copy,
//         R2: 'a + RangeBounds<usize>,
//     {
//         // let len_slice_1 = index.1.end_bound()
//         let mut data = Vec::<&[E]>::with_capacity(self.n_rows());
//         for i in 0..self.n_rows() {
//             if index.1.contains(&i) {
//                 data.push(&self.data[i][index.0]);
//             }
//         }
//         // let temp: &dyn SliceIndex<&[E], Output = &[E]> = .. as &SliceIndex<&[E], Output = &[E]>;
//         // let a = &self.data[temp];
//         // let temp: &[E] = &self.data[1][index.0];
//         // let data: Vec<&[E]> = self
//         //     .data //[index.1]
//         //     .iter()
//         //     .enumerate()
//         //     .filter(|(i, _)| index.1.contains(&i))
//         //     .map(|(_, v)| &v[index.0])
//         //     .collect();
//         GridSlice(vec![])
//     }
// }
#[cfg(test)]
mod test;
