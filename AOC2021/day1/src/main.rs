use utils;

fn main() {
    let input = utils::input_lines(1);
    let data = parse_input(input);
    let day1 = n_increases(&data);

    println!("Day 1 answer: {}", day1);

    let windowed = windowed_sum(3, &data);
    let day2 = n_increases(&windowed);
    println!("Day 2 answer: {}", day2);

}

fn windowed_sum(size: usize, data: &Vec<i32>) -> Vec<i32> {
    data.windows(size)
        .map(|x| x.into_iter().sum())
        .collect()
}

fn n_increases(data: &Vec<i32>) -> i32 {
    let mut n = 0;
    let mut prev = &data[0];
    for entry in &data[1..] {
        if entry > prev { n += 1; }
        prev = entry
    }
    n
}

fn parse_input(input: Vec<String>) -> Vec<i32> {
    let lines: Vec<i32> = input
        .into_iter()
        .map(|x| x.parse::<i32>().expect("Failed to parse"))
        .collect();
    lines
}

#[cfg(test)]
mod test {
    use std::env;

    use super::*;

    #[test]
    fn test_n_increases() {
        let data = parse_input(utils::string_input_lines(TEST_1));
        let result = n_increases(&data);
        assert_eq!(result, 7);
    }

    #[test]
    fn test_sliding_window() {
        let data = parse_input(utils::string_input_lines(TEST_1));
        let result = windowed_sum(3, &data);
        assert_eq!(result[0], 607);
        assert_eq!(result[1], 618);
        assert_eq!(*(result.last().expect("empty list")), 269+260+263);
    }

    #[test]
    fn test_sample_part2(){
        let data = parse_input(utils::string_input_lines(TEST_1));
        let result = n_increases(&windowed_sum(3, &data));
        assert_eq!(result, 5)
    }

    #[test]
    fn test_part1() {
        println!("{:?}", env::current_dir());
        let input = utils::input_lines(1);
        let data = parse_input(input);
        let day1 = n_increases(&data);
        assert_eq!(day1, 1529)
    }

    #[test]
    fn test_part2() {
        println!("{:?}", env::current_dir());
        let input = utils::input_lines(1);
        let data = parse_input(input);
        let windowed = windowed_sum(3, &data);
        let day2 = n_increases(&windowed);
        assert_eq!(day2, 1567)
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