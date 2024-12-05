use utils;

struct Report(Vec<u32>);

impl Report {
    fn new_list(input: Vec<String>) -> Vec<Report> {
        input
            .iter()
            .map(|line| {
                Report(
                    line.split_ascii_whitespace()
                        .map(|v| v.parse().unwrap())
                        .collect(),
                )
            })
            .collect()
    }

    fn diff(a: u32, b: u32) -> i32 {
        a as i32 - b as i32
    }

    fn is_safe(&self) -> bool {
        let vs = &self.0;
        let increasing: bool = Self::diff(vs[0], vs[1]) < 0;
        for i in 1..self.0.len() {
            let curr = vs[i];
            let prev = vs[i - 1];
            let d = Self::diff(curr, prev);
            if d.abs() == 0 || d.abs() > 3 || ((d > 0) != increasing) {
                return false;
            }
        }
        true
    }
}

fn n_safe(reports: Vec<Report>) -> usize {
    reports
        .iter()
        .map(|r| if r.is_safe() { 1 } else { 0 })
        .sum()
}

fn main() {
    let input = utils::input_lines(2);
    let reports = Report::new_list(input);
    let part_1_answer = n_safe(reports);
    println!("Day 2, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
