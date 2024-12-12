use std::sync::LazyLock;

use fancy_regex::Regex;

static MUL_RE: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap());

static COND_RE: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"(^|do(?!(n't)))(.*?)(don't|$)").unwrap());

fn process_muls(input: &[String]) -> u64 {
    mul_sum(&input.join(" "))
}

fn conditional_muls(input: &[String]) -> u64 {
    COND_RE
        .captures_iter(&input.join(" "))
        .map(|c| {
            let c = c.unwrap();
            // println!("{:?}\n---\n{}\n\n", c, c[0].to_string());
            mul_sum(&c[3])
        })
        .sum()
}

fn mul_sum(s: &str) -> u64 {
    MUL_RE
        .captures_iter(s)
        .map(|m| {
            let m = m.unwrap();
            m[1].parse::<u64>().unwrap() * m[2].parse::<u64>().unwrap()
        })
        .sum()
}

fn main() {
    let input = utils::input_lines(3);
    let part_1_answer = process_muls(&input);
    println!("Day 3, Part 1 answer: {}", part_1_answer);
    let part_2_answer = conditional_muls(&input);
    println!("Day 3, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
