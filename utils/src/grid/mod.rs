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

pub trait GridTrait<'a, E>: Index<Pos> + IndexMut<Pos> + From<Self::SliceType>
where
    Self: 'a,
{
    type SliceType;
    type CoordType: PrimInt;

    fn is_inside(&self, coord: &Pos) -> bool;
    // min_x, min_y, max_x, max_y
    fn bounds(&self) -> GridBounds<Self::CoordType>;
    fn size(&self) -> (CoordType, CoordType);
    fn n_elem(&self) -> CoordType;
    fn map<'b, F, T: 'b>(&'b self, fun: F) -> impl GridTrait<T>
    where
        F: Fn(&E) -> T,
        T: Clone + Default + Copy;
    fn apply(&mut self, fun: impl Fn(&E) -> E);
}

pub struct GridBounds<T: num::PrimInt> {
    pub min_x: T,
    pub min_y: T,
    pub max_x: T,
    pub max_y: T,
}

#[cfg(test)]
mod test;
