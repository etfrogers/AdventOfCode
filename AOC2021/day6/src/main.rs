use std::{collections::HashMap, ops::Index};

use utils::{self, Counter};

struct School {
    data: HashMap<u16, u64>,
}

impl Index<u16> for School {
    type Output = u64;

    fn index(&self, index: u16) -> &Self::Output {
        &self.data[&index]
    }
}

// impl IndexMut<u16> for School {
//     fn index_mut(&mut self, index: u16) -> &mut Self::Output {
//         self.data.entry(index).
//     }
// }

impl School {
    fn new(lifetimes: Vec<u16>) -> Self {
        let data = Counter::new(lifetimes);
        Self { data: data.map() }
    }

    fn evolve(&mut self, days: u64) {
        for _ in 0..days {
            let day0 = *self.data.get(&0).unwrap_or(&0);
            let mut new_data: HashMap<u16, u64> = HashMap::new();
            for i in self.data.keys() {
                match i {
                    0 => (),
                    1..=8 => {
                        new_data.insert(i - 1, self.data[i]);
                        ()
                    }
                    _ => panic!("Unexpected value"),
                }
            }
            *new_data.entry(6).or_insert(0) += day0;
            *new_data.entry(8).or_insert(0) += day0;
            self.data = new_data;
        }
    }

    fn total_fish(&self) -> u64 {
        self.data.values().sum()
    }
}

fn main() {
    let input = utils::input_lines(6);
    let mut school = School::new(utils::csv_line(&input[0]).unwrap());
    school.evolve(80);
    let part_1_answer = school.total_fish();
    println!("Day 6, Part 1 answer: {}", part_1_answer);

    let mut school = School::new(utils::csv_line(&input[0]).unwrap());
    school.evolve(256);
    let part_2_answer = school.total_fish();
    println!("Day 6, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
