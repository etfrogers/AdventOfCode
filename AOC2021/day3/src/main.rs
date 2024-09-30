
use std::{
    collections::HashMap, num::ParseIntError
};

use utils;

fn main() {
    let input = utils::input_lines(3);
    let report = Report::build(input);
    // println!("{:#?}", report);
    let part_1_answer = report.power_consumption();
    println!("Day 3, Part 1 answer: {}", part_1_answer);

    let part_2_answer = report.life_support_rating();
    println!("Day 3, Part 2 answer: {}", part_2_answer);

}

#[derive(Debug, Clone)]
struct Report {
    len: usize,
    chars: Vec<Vec<bool>>,
    epsilon_rate: u32,
    gamma_rate: u32,
    oxygen_rating: u32,
    co2_rating: u32,
    most_common_bits: Vec<bool>
}

#[derive(Debug)]
struct NoMostCommon;


impl Report {


    fn to_bool(c: char) -> bool {
        match c {
            '1' => true,
            '0' => false,
            _ => panic!("chars must be 0 or 1")
        }
    }

    fn to_char(b: &bool) -> char {
        if *b{'1'} else {'0'}
    }

    fn build(strs: Vec<String>) -> Report {
        
        let chars: Vec<Vec<bool>> = strs
            .into_iter()
            .map(|s| s.chars()
                .map(Report::to_bool )
                .collect())
            .collect();
        let len = chars[1].len();
        let mut report = Report{
            len,
            chars,
            epsilon_rate: 0,
            gamma_rate: 0,
            oxygen_rating: 0,
            co2_rating: 0,
            most_common_bits: vec![],
        };
        report.calculate_rates();
        report.calculate_ratings();
        report
    }

    fn power_consumption(&self) -> u32 {
        return self.gamma_rate * self.epsilon_rate;
    }

    fn life_support_rating(&self) -> u32 {
        return self.co2_rating * self.oxygen_rating;
    }

    fn most_common_bit(array: &Vec<Vec<bool>>, pos: usize) -> Result<bool, NoMostCommon> {
        let mut counts: HashMap<bool, u32> = HashMap::new();
        for row in array {
            let count = counts.entry(row[pos]).or_insert(0);
            *count += 1;
        }
        let n_false = *counts.get(&false).unwrap_or(&0);
        let n_true = *counts.get(&true).unwrap_or(&0);
        if  n_false > n_true {
            Ok(false)
        } else if n_false < n_true {
            Ok(true)
        } else {
            Err(NoMostCommon)
        }
    }

    fn calculate_most_common_bits(& mut self) {
        self.most_common_bits = (0..self.len)
            .map(|i| Report::most_common_bit(&self.chars, i)
                .expect("Should always be most common bit in whole array"))
            .collect()
    
    }
    
    fn least_common_bits(&self) -> Vec<bool> {
        self.most_common_bits.clone().into_iter().map(|c| !c).collect()
    }
    
    fn calculate_rates(& mut self) {
        self.calculate_most_common_bits();
        let gamma_chars = self.most_common_bits.clone();
        let epsilon_chars = self.least_common_bits();
        self.epsilon_rate = Report::to_int(&epsilon_chars).unwrap();
        self.gamma_rate = Report::to_int(&gamma_chars).unwrap();
    }

    fn to_int(chars: &Vec<bool>) -> Result<u32, ParseIntError> {
        let chars: Vec<char> = chars.iter().map(Report::to_char).collect();
        u32::from_str_radix(&String::from_iter(chars), 2)
    }

    fn calculate_ratings(&mut self) {
        self.oxygen_rating = Report::to_int(&self.filter_report_by(true)).unwrap();
        self.co2_rating = Report::to_int(&self.filter_report_by(false)).unwrap();
    }

    fn filter_report_by(&self, use_most_common: bool) -> Vec<bool> {
        let mut valid = self.chars.clone();
        loop {
            for i in 0..self.len {
                let most_common = Report::most_common_bit(&valid, i);
                let filter_bit = match most_common {
                    Ok(most_common) => if use_most_common {
                            most_common }
                        else{
                            !most_common
                        },
                    Err(NoMostCommon) => use_most_common,
                };
                valid = valid.into_iter()
                    .filter(|line| line[i] == filter_bit)
                    .collect();
                if valid.len() == 1{
                    return valid[0].clone();
                }
            }
        }
    }

}


#[cfg(test)]
mod test;

