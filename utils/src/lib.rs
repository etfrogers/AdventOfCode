use std::{collections::HashMap, env, error::Error, fmt::Display, fs, hash::Hash, ops::Deref};

pub mod grid;

#[derive(Debug)]
pub struct StringParseError {
    item: String,
    source: Option<anyhow::Error>,
}

impl StringParseError {
    pub fn new(s: &str) -> Self {
        Self {
            item: s.to_string(),
            source: None,
        }
    }

    pub fn new_with_source(s: &str, source: anyhow::Error) -> Self {
        Self {
            item: s.to_string(),
            source: Some(source),
        }
    }
}

impl Display for StringParseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Unable to parse String: {}", self.item)
    }
}

pub fn input_lines(_day: u8) -> Vec<String> {
    let dir = env::var("CARGO_MANIFEST_DIR").unwrap_or_default();
    let data = match fs::read_to_string(format!("{dir}/input.txt")) {
        Ok(d) => d,
        Err(_) => fs::read_to_string("input.txt").unwrap_or_else(|_| {
            panic!(
                "Failed to read input file. Current dir: {:?}",
                env::current_dir()
            )
        }),
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
