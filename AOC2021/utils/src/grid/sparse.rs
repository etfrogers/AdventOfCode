use std::{
    collections::HashMap,
    ops::{Deref, DerefMut},
};

use super::Pos;

pub struct SparseGrid<T> {
    data: HashMap<Pos, T>,
}

impl<T> Deref for SparseGrid<T> {
    type Target = HashMap<Pos, T>;

    fn deref(&self) -> &Self::Target {
        &self.data
    }
}

impl<T> DerefMut for SparseGrid<T> {
    // type Target = HashMap<Pos, T>;

    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.data
    }
}

impl<T> SparseGrid<T> {
    pub fn new() -> Self {
        Self {
            data: HashMap::<Pos, T>::new(),
        }
    }
}
