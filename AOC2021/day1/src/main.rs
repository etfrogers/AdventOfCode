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
mod test;