use utils;

fn parse_input(input: Vec<String>) -> (Vec<i32>, Vec<i32>) {
    let (a, b): (Vec<_>, Vec<_>) = input
        .iter()
        .map(|line| {
            let mut iter = line.split_ascii_whitespace();
            (
                iter.next().unwrap().parse::<i32>().unwrap(),
                iter.next().unwrap().parse::<i32>().unwrap(),
            )
        })
        .unzip();
    (a, b)
}

fn total_diff(l1: &Vec<i32>, l2: &Vec<i32>) -> i32 {
    let mut l1 = l1.clone();
    let mut l2 = l2.clone();
    l1.sort();
    l2.sort();
    l1.iter().zip(l2).map(|(v1, v2)| (v1 - v2).abs()).sum()
}

fn main() {
    let input = utils::input_lines(1);
    let (l1, l2) = parse_input(input);
    let part_1_answer = total_diff(&l1, &l2);
    println!("Day 1, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
