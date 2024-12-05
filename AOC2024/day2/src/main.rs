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

    fn is_safe(&self, with_dampener: bool) -> bool {
        let orig = Self::is_safe_vec(&self.0);
        if !with_dampener {
            orig
        } else if orig {
            true
        } else {
            for i in 0..self.0.len() {
                let mut short = self.0.clone();
                short.remove(i);
                if Self::is_safe_vec(&short) {
                    return true;
                }
            }
            false
        }
    }

    fn is_safe_vec(vs: &Vec<u32>) -> bool {
        let increasing: bool = Self::diff(vs[0], vs[1]) < 0;
        for i in 1..vs.len() {
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

fn n_safe(reports: &Vec<Report>, with_dampener: bool) -> usize {
    reports
        .iter()
        .map(|r| if r.is_safe(with_dampener) { 1 } else { 0 })
        .sum()
}

fn main() {
    let input = utils::input_lines(2);
    let reports = Report::new_list(input);
    let part_1_answer = n_safe(&reports, false);
    println!("Day 2, Part 1 answer: {}", part_1_answer);
    let part_2_answer = n_safe(&reports, true);
    println!("Day 2, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
