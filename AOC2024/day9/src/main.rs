use std::fmt::Display;

use itertools::Itertools;

use utils;

struct DiskMap(Vec<Option<u32>>);
struct Defragged(Vec<u32>);

impl DiskMap {
    fn new(input: &Vec<String>) -> Self {
        assert_eq!(input.len(), 1);
        let input = &input[0];
        let mut map = Vec::new();
        let mut id = 0;
        for mut sizes in &input.chars().chunks(2) {
            let file_size: usize = sizes.next().unwrap().to_string().parse().unwrap();
            let blank_size: usize = sizes.next().unwrap_or('0').to_string().parse().unwrap();
            map.extend(vec![Some(id); file_size]);
            map.extend(vec![None; blank_size]);
            id += 1;
        }
        Self(map)
    }

    fn defrag(&self) -> Defragged {
        let mut n_file_blocks = 0;
        self.0.iter().for_each(|v| {
            if v.is_some() {
                n_file_blocks += 1
            }
        });
        let mut files = self.0.clone();
        let mut defragged = Vec::new();
        defragged.resize(n_file_blocks, 0);
        for (i, block) in defragged.iter_mut().enumerate() {
            *block = files[i].unwrap_or_else(|| loop {
                match files.pop().unwrap() {
                    Some(id) => break id,
                    None => (),
                }
            })
        }
        Defragged(defragged)
    }
}

impl Defragged {
    fn checksum(&self) -> u64 {
        self.0
            .iter()
            .enumerate()
            .map(|(i, v)| i as u64 * (*v) as u64)
            .sum()
    }
}

impl Display for DiskMap {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}",
            self.0
                .iter()
                .map(|v| match v {
                    Some(s) => s.to_string(),
                    None => ".".to_owned(),
                })
                .join("")
        )
    }
}

impl Display for Defragged {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0.iter().map(|v| v.to_string()).join(""))
    }
}

fn main() {
    let input = utils::input_lines(9);
    let dm = DiskMap::new(&input);
    let part_1_answer = dm.defrag().checksum();
    println!("Day 9, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
