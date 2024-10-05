use std::fs;

pub mod grid;

pub fn input_lines(day: u8) -> Vec<String> {
    let data = match fs::read_to_string(format!("day{day}/input.txt")) {
        Ok(d) => d,
        Err(_) => fs::read_to_string("input.txt").expect("Failed to read input file")
    };
    string_input_lines(&data)
}

pub fn string_input_lines(data: &str) -> Vec<String> {
    data.lines()
    .map(String::from)
    .collect()
}