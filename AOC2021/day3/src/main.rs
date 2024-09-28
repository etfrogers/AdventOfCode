// use std::str::FromStr;

use std::collections::HashMap;

use utils;

fn main() {
    let input = utils::input_lines(3);
    let report = Report::build(input);
    // println!("{:#?}", report);
    let part_1_answer = report.power_consumption();
    println!("Day 1 answer: {}", part_1_answer);

}

#[derive(Debug, Clone)]
struct Report {
    len: usize,
    chars: Vec<Vec<char>>,
    ints: Vec<u32>,
    epsilon_rate: u32,
    gamma_rate: u32,
}

impl Report {
    fn build(strs: Vec<String>) -> Report {
        
        let chars: Vec<Vec<char>> = strs.clone().into_iter().map(|s| s.chars().collect()).collect();
        let len = chars[1].len();
        let ints = strs.into_iter()
            .map(|s| u32::from_str_radix(&s, 2).unwrap())
            .collect();
        let mut report = Report{
            len,
            chars,
            ints,
            epsilon_rate: 0,
            gamma_rate: 0,
        };
        report.calculate_rates();
        report
    }

    fn power_consumption(&self) -> u32 {
        return self.gamma_rate * self.epsilon_rate;
    }

    fn calculate_rates(& mut self) {
        let mut gamma_chars = vec!['-'; self.len];
        let mut epsilon_chars = vec!['-'; self.len];
        
        for i in 0..self.len {
            let mut counts: HashMap<char, u32> = HashMap::new();
            for row in self.chars.clone() {
                let count = counts.entry(row[i]).or_insert(0);
                *count += 1;
            }
            if counts[&'0'] > counts[&'1'] {
                gamma_chars[i] = '0';
                epsilon_chars[i] = '1';
            } else {
                gamma_chars[i] = '1';
                epsilon_chars[i] = '0';
            }
        }
        self.epsilon_rate = u32::from_str_radix(&String::from_iter(epsilon_chars), 2).unwrap();
        self.gamma_rate = u32::from_str_radix(&String::from_iter(gamma_chars), 2).unwrap();
    }
}



#[cfg(test)]
mod test;

