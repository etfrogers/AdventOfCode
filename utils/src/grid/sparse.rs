use std::{
    collections::{hash_map::IntoIter, HashMap},
    fmt::Display,
    ops::{Deref, DerefMut, Index, IndexMut, RangeBounds},
};

use crate::grid::Grid;

use super::{GridBounds, GridFind, GridTrait, Pos};

#[derive(Debug, PartialEq, Clone)]
pub struct SparseGrid<E> {
    data: HashMap<Pos, E>,
    default: Option<E>,
    bounds: Option<GridBounds<i32>>,
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
            bounds: None,
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
            ..Default::default()
        }
    }
}

impl<'a, E: Default + Copy + 'a> GridTrait<'a, E> for SparseGrid<E> {
    type CoordType = i32;
    type SliceType = SparseSlice<'a, E> where E: 'a;

    fn is_inside(&self, pos: &Pos<Self::CoordType>) -> bool {
        match self.bounds {
            Some(bounds) => {
                pos.x() >= bounds.min_x
                    && pos.x() < bounds.max_x
                    && pos.y() >= bounds.min_y
                    && pos.y() < bounds.max_y
            }
            None => true,
        }
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
            new_map.insert(key, fun(value));
        }
        SparseGrid::from(new_map)
    }

    fn iter_mut(&'a mut self) -> impl Iterator<Item = (Pos<Self::CoordType>, &'a mut E)> {
        self.data.iter_mut().map(|(k, v)| (*k, v))
    }

    fn values_mut(&'a mut self) -> impl Iterator<Item = &'a mut E> {
        self.data.values_mut()
    }

    fn iter(&'a self) -> impl Iterator<Item = (Pos<Self::CoordType>, &'a E)> {
        self.data.iter().map(|(k, v)| (*k, v))
    }

    fn full(
        _x: super::pos::CoordType,
        _y: super::pos::CoordType,
        _content: E,
    ) -> impl GridTrait<'a, E> {
        SparseGrid::new()
    }

    fn full_like(_template: &'a Grid<E>, _content: E) -> impl GridTrait<'a, E> {
        SparseGrid::new()
    }
}

impl<'a, E: 'a + PartialEq + Clone + Copy + Default> GridFind<'a, E> for SparseGrid<E> {}

impl<E> SparseGrid<E> {
    pub fn slice<'a, R1, R2>(&'a self, index: (R1, R2)) -> SparseSlice<'a, E>
    where
        R1: 'a + RangeBounds<i32>,
        R2: 'a + RangeBounds<i32>,
        E: Default + Copy,
    {
        let mapped = self
            .iter()
            .filter(move |(k, _)| index.0.contains(&k.x()) && index.1.contains(&k.y()));
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
    pub fn from_dense(
        dense: Grid<E>,
        default: E,
    ) -> Result<Self, <GridBounds<i32> as TryFrom<GridBounds<usize>>>::Error> {
        let mut map = HashMap::<Pos, E>::new();
        let bounds = Some(dense.bounds().try_into()?);
        for (pos, v) in dense {
            let pos: Pos<i32> = pos.try_into()?;
            if v != default {
                map.insert(pos, v);
            }
        }
        Ok(SparseGrid {
            data: map,
            default: Some(default),
            bounds,
        })
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

impl<E> IntoIterator for SparseGrid<E> {
    type Item = (Pos, E);

    type IntoIter = IntoIter<Pos, E>;

    fn into_iter(self) -> Self::IntoIter {
        self.data.into_iter()
    }
}
