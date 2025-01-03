use std::ops::{Index, IndexMut};

pub use dense::Grid;
use num::PrimInt;
use pos::{CoordType, Pos};
pub use sparse::SparseGrid;

pub mod coord;
pub mod dense;
pub mod direction;
mod iter;
pub mod pos;
pub mod sparse;

pub trait GridTrait<'a, E: 'a>:
    Index<Pos<Self::CoordType>>
    + IndexMut<Pos<Self::CoordType>>
    + From<Self::SliceType>
    + IntoIterator<Item = (Pos<Self::CoordType>, E)>
where
    Self: 'a,
{
    type SliceType;
    type CoordType: PrimInt;

    fn is_inside(&self, coord: &Pos<Self::CoordType>) -> bool;
    fn bounds(&self) -> GridBounds<Self::CoordType>;
    fn size(&self) -> (CoordType, CoordType);
    fn n_elem(&self) -> CoordType;
    fn map<'b, F, T>(&'b self, fun: F) -> impl GridTrait<'b, T>
    where
        F: Fn(&E) -> T,
        T: 'b + Copy + Default;

    fn apply(&'a mut self, fun: impl Fn(&E) -> E) {
        for v in self.values_mut() {
            *v = fun(v)
        }
    }
    fn iter(&'a self) -> impl Iterator<Item = (Pos<Self::CoordType>, &'a E)>;
    fn iter_mut(&'a mut self) -> impl Iterator<Item = (Pos<Self::CoordType>, &'a mut E)>;
    fn values_mut(&'a mut self) -> impl Iterator<Item = &'a mut E>;
    fn full(x: CoordType, y: CoordType, content: E) -> impl GridTrait<'a, E>;
    fn full_like(template: &'a Grid<E>, content: E) -> impl GridTrait<'a, E>;
}

pub trait GridFind<'a, E: 'a + PartialEq>: GridTrait<'a, E> {
    // Returns x and y coords of first occurence of the input val
    // If the value is not found, None
    fn find(&'a self, val: E) -> Option<Pos<Self::CoordType>> {
        self.iter().find(|(_, v)| **v == val).map(|v| v.0)
    }

    fn find_all(&'a self, val: E) -> impl Iterator<Item = Pos<Self::CoordType>> {
        self.iter().filter(move |(_, v)| **v == val).map(|v| v.0)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct GridBounds<T: num::PrimInt> {
    pub min_x: T,
    pub min_y: T,
    pub max_x: T,
    pub max_y: T,
}

impl TryFrom<GridBounds<usize>> for GridBounds<i32> {
    type Error = <usize as TryFrom<i32>>::Error;

    fn try_from(value: GridBounds<usize>) -> Result<Self, Self::Error> {
        Ok(Self {
            min_x: value.min_x.try_into()?,
            min_y: value.min_y.try_into()?,
            max_x: value.max_x.try_into()?,
            max_y: value.max_y.try_into()?,
        })
    }
}

#[cfg(test)]
mod test;
