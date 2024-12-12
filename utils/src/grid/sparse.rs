use std::{
    collections::HashMap,
    fmt::Display,
    ops::{Deref, DerefMut, Index, IndexMut, RangeBounds},
};

use crate::grid::Grid;

use super::{GridBounds, GridTrait, Pos};

#[derive(Debug, PartialEq, Clone)]
pub struct SparseGrid<E> {
    data: HashMap<Pos, E>,
    default: Option<E>,
}

impl<E> Deref for SparseGrid<E> {
    type Target = HashMap<Pos, E>;

    fn deref(&self) -> &Self::Target {
        &self.data
    }
}

impl<E> DerefMut for SparseGrid<E> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.data
    }
}

impl<E> SparseGrid<E> {
    pub fn new() -> Self {
        Self {
            data: HashMap::<Pos, E>::new(),
            default: None,
        }
    }
}

impl<E> Default for SparseGrid<E> {
    fn default() -> Self {
        Self::new()
    }
}

impl<E> From<HashMap<Pos, E>> for SparseGrid<E> {
    fn from(data: HashMap<Pos, E>) -> Self {
        Self {
            data,
            default: None,
        }
    }
}

impl<'a, E: Default + Copy + 'a> GridTrait<'a, E> for SparseGrid<E> {
    fn is_inside(&self, _: &Pos) -> bool {
        true
    }

    fn bounds(&self) -> GridBounds<Self::CoordType> {
        if self.len() == 0 {
            GridBounds {
                min_x: 0,
                min_y: 0,
                max_x: 0,
                max_y: 0,
            }
        } else {
            let (xs, ys): (Vec<_>, Vec<_>) = self.data.keys().map(|p| p.tuple()).unzip();
            GridBounds {
                min_x: *xs.iter().min().unwrap(),
                min_y: *ys.iter().min().unwrap(),
                max_x: *xs.iter().max().unwrap(),
                max_y: *ys.iter().max().unwrap(),
            }
        }
    }

    fn size(&self) -> (super::CoordType, super::CoordType) {
        let bounds = self.bounds();
        (
            (1 + bounds.max_x - bounds.min_x).try_into().unwrap(),
            (1 + bounds.max_y - bounds.min_y).try_into().unwrap(),
        )
    }

    fn n_elem(&self) -> super::CoordType {
        self.data.len()
    }

    #[allow(refining_impl_trait)]
    fn map<'b, F, T>(&'b self, fun: F) -> SparseGrid<T>
    where
        F: Fn(&E) -> T,
        T: 'b + Clone + Default + Copy,
    {
        let mut new_map = HashMap::<Pos, T>::new();
        for (key, value) in self.iter() {
            new_map.insert(*key, fun(value));
        }
        SparseGrid::from(new_map)
    }

    fn apply(&mut self, fun: impl Fn(&E) -> E) {
        for (_, value) in self.iter_mut() {
            *value = fun(value);
        }
    }

    type CoordType = i32;
    type SliceType = SparseSlice<'a, E> where E: 'a;
}

impl<E> SparseGrid<E> {
    pub fn slice<'a, R1, R2>(&'a self, index: (R1, R2)) -> SparseSlice<'a, E>
    where
        R1: 'a + RangeBounds<i32>,
        R2: 'a + RangeBounds<i32>,
        E: Default + Copy,
    {
        let mapped = self
            .iter()
            .filter(move |(k, _)| index.0.contains(&k.x()) && index.1.contains(&k.y()))
            .map(move |(k, v)| (*k, v));
        SparseSlice(Box::new(mapped))
    }

    pub fn default(&self) -> &Option<E> {
        &self.default
    }

    pub fn set_default(&mut self, value: E) {
        self.default = Some(value)
    }

    pub fn shift(&mut self, shift: Pos) {
        take_mut::take(&mut self.data, |data| {
            data.into_iter().map(|(p, v)| (p + shift, v)).collect()
        });
    }
}

impl<E: PartialEq + Copy> SparseGrid<E> {
    pub fn from_dense(dense: Grid<E>, default: E) -> Self {
        let mut map = HashMap::<Pos, E>::new();
        for pos in dense.coords() {
            let pos: Pos<i32> = pos.try_into().unwrap();
            if dense[pos] != default {
                map.insert(pos, default);
            }
        }
        SparseGrid {
            data: map,
            default: Some(default),
        }
    }
}

pub struct SparseSlice<'a, E: 'a>(Box<dyn Iterator<Item = (Pos, &'a E)> + 'a>);

impl<'a, E: Copy> From<SparseSlice<'a, E>> for SparseGrid<E> {
    fn from(value: SparseSlice<'a, E>) -> Self {
        let data = value.0.map(|(k, v)| (k, *v)).collect::<HashMap<_, _>>();
        SparseGrid::from(data)
    }
}

impl<'a, E> Deref for SparseSlice<'a, E> {
    type Target = dyn Iterator<Item = (Pos, &'a E)> + 'a;

    fn deref(&self) -> &Self::Target {
        &(*self.0)
    }
}

impl<'a, E> DerefMut for SparseSlice<'a, E> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut (*self.0)
    }
}
impl<E> Index<Pos> for SparseGrid<E> {
    type Output = E;

    fn index(&self, index: Pos) -> &Self::Output {
        &self.data[&index]
    }
}

impl<E: Default> IndexMut<Pos> for SparseGrid<E> {
    fn index_mut(&mut self, index: Pos) -> &mut Self::Output {
        self.data.entry(index).or_default()
    }
}

impl<E> Index<(i32, i32)> for SparseGrid<E> {
    type Output = E;

    fn index(&self, index: (i32, i32)) -> &Self::Output {
        &self[Into::<Pos>::into(index)]
    }
}

impl<E: Default> IndexMut<(i32, i32)> for SparseGrid<E> {
    fn index_mut(&mut self, index: (i32, i32)) -> &mut Self::Output {
        &mut self[Into::<Pos>::into(index)]
    }
}

impl<E: Display + Default + Copy> Display for SparseGrid<E> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if self.default.is_none() {
            write!(f, "Unable to display Sparse grid without default value")
        } else if let Ok(grid) = TryInto::<Grid<E>>::try_into(self.clone()) {
            write!(f, "{}", grid)
        } else {
            write!(f, "Unable to format grid")
        }
    }
}
