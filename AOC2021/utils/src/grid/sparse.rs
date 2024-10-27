use std::{
    collections::HashMap,
    ops::{Deref, DerefMut, Index, IndexMut, RangeBounds},
};

use super::{GridTrait, Pos};

#[derive(Debug, PartialEq)]
pub struct SparseGrid<E> {
    data: HashMap<Pos, E>,
}

impl<E> Deref for SparseGrid<E> {
    type Target = HashMap<Pos, E>;

    fn deref(&self) -> &Self::Target {
        &self.data
    }
}

impl<E> DerefMut for SparseGrid<E> {
    // type Target = HashMap<Pos, E>;

    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.data
    }
}

impl<E> SparseGrid<E> {
    pub fn new() -> Self {
        Self {
            data: HashMap::<Pos, E>::new(),
        }
    }
}

impl<E> From<HashMap<Pos, E>> for SparseGrid<E> {
    fn from(data: HashMap<Pos, E>) -> Self {
        Self { data }
    }
}

impl<'a, E: Default + Copy + 'a> GridTrait<'a, E> for SparseGrid<E> {
    fn is_inside(&self, _: &Pos) -> bool {
        true
    }

    fn size(&self) -> (super::CoordType, super::CoordType) {
        let (xs, ys): (Vec<_>, Vec<_>) = self.data.keys().map(|p| p.tuple()).unzip();
        let width = xs.iter().max().unwrap() - xs.iter().min().unwrap();
        let height = ys.iter().max().unwrap() - ys.iter().min().unwrap();
        (width.try_into().unwrap(), height.try_into().unwrap())
    }

    fn n_elem(&self) -> super::CoordType {
        return self.data.len();
    }

    #[allow(refining_impl_trait)]
    fn map<'b, F, T: 'b>(&'b self, fun: F) -> SparseGrid<T>
    where
        F: Fn(&E) -> T,
        T: Clone + Default + Copy,
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
        return &(*self.0);
    }
}

impl<'a, E> DerefMut for SparseSlice<'a, E> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        return &mut (*self.0);
    }
}
impl<E> Index<Pos> for SparseGrid<E> {
    type Output = E;

    fn index(&self, index: Pos) -> &Self::Output {
        &self.data[&index]
    }
}

impl<'a, E: Default> IndexMut<Pos> for SparseGrid<E> {
    fn index_mut(&mut self, index: Pos) -> &mut Self::Output {
        self.data.entry(index).or_insert(E::default())
    }
}

impl<E> Index<(i32, i32)> for SparseGrid<E> {
    type Output = E;

    fn index(&self, index: (i32, i32)) -> &Self::Output {
        &self[Into::<Pos>::into(index)]
    }
}

impl<'a, E: Default> IndexMut<(i32, i32)> for SparseGrid<E> {
    fn index_mut(&mut self, index: (i32, i32)) -> &mut Self::Output {
        &mut self[Into::<Pos>::into(index)]
    }
}
