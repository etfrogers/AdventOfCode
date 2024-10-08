use std::{collections::HashMap, fs, hash::Hash, num::ParseIntError, ops::Deref};

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

pub fn csv_line(line: &str) -> Result<Vec<u16>, ParseIntError> {
    line.split(',')
        .map(|s| s.parse::<u16>())
        .collect::<Result<Vec<u16>, ParseIntError>>()
}

pub struct Counter<T>(HashMap<T, u64>)
where
    T: Eq + Hash;

impl<T: Eq + Hash> Counter<T> {
    pub fn new(input: impl Iterator<Item = T>) -> Self {
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
