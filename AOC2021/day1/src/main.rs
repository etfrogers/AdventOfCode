use std::fs;

fn main() {
    let input = fs::read_to_string("day1/src/input.txt")
        .expect("Should have been able to read the file");
    let data = parse_input(&input);
    let day1 = n_increases(data);

    println!("Day 1 answer: {}", day1)
}

fn n_increases(data: Vec<i32>) -> i32 {
    let mut n = 0;
    let mut prev = &data[0];
    for entry in &data[1..] {
        if entry > prev { n += 1; }
        prev = entry
    }
    n
}

fn parse_input(input: &str) -> Vec<i32> {
    let lines: Vec<i32> = input
        .lines()
        .map(|x| x.parse::<i32>().expect("Failed to parse"))
        .collect();
    lines
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_n_increases() {
        let data = parse_input(TEST_1);
        let result = n_increases(data);
        assert_eq!(result, 7);
    }

    const TEST_1: &str = "199
200
208
210
200
207
240
269
260
263";
}