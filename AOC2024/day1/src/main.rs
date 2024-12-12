use utils::{self, Counter};

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

fn total_diff(l1: &[i32], l2: &[i32]) -> i32 {
    let mut l1 = l1.to_vec();
    let mut l2 = l2.to_vec();
    l1.sort();
    l2.sort();
    l1.iter().zip(l2).map(|(v1, v2)| (v1 - v2).abs()).sum()
}

fn similarity_score(l1: &[i32], l2: &Vec<i32>) -> i32 {
    let counts = Counter::new(l2);
    l1.iter()
        .map(|v| {
            let c: i32 = (*counts.get(&v).unwrap_or(&0)).try_into().unwrap();
            v * c
        })
        .sum()
}

fn main() {
    let input = utils::input_lines(1);
    let (l1, l2) = parse_input(input);
    let part_1_answer = total_diff(&l1, &l2);
    println!("Day 1, Part 1 answer: {}", part_1_answer);

    let part_2_answer = similarity_score(&l1, &l2);
    println!("Day 1, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
