use std::{collections::HashMap, fs, hash::Hash, ops::Deref};

use num;

pub mod grid;

pub fn input_lines(day: u8) -> Vec<String> {
    let data = match fs::read_to_string(format!("day{day}/input.txt")) {
        Ok(d) => d,
        Err(_) => fs::read_to_string("input.txt").expect("Failed to read input file"),
    };
    string_input_lines(&data)
}

pub fn string_input_lines(data: &str) -> Vec<String> {
    data.lines().map(String::from).collect()
}

pub fn csv_line<T: num::PrimInt + std::str::FromStr>(
    line: &str,
) -> Result<Vec<T>, <T as std::str::FromStr>::Err> {
    line.split(',')
        .map(|s| s.parse::<T>())
        .collect::<Result<Vec<T>, _>>()
}

pub struct Counter<T>(HashMap<T, u64>)
where
    T: Eq + Hash;

impl<T: Eq + Hash> Counter<T> {
    pub fn new(input: impl IntoIterator<Item = T>) -> Self {
        let mut counts: HashMap<T, u64> = HashMap::new();
        for item in input {
            let count = counts.entry(item).or_insert(0);
            *count += 1;
        }
        Self(counts)
    }
}

impl<T: Eq + Hash> Deref for Counter<T> {
    type Target = HashMap<T, u64>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<T: Eq + Hash + Clone> Counter<T> {
    pub fn data(self) -> HashMap<T, u64> {
        self.0
    }
}
