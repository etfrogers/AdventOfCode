use std::fmt::Display;

use itertools::Itertools;

struct DiskMap(Vec<Option<u32>>);
struct Gap {
    start: usize,
    len: usize,
}

impl DiskMap {
    fn new(input: &[String]) -> Self {
        assert_eq!(input.len(), 1);
        let input = &input[0];
        let mut map = Vec::new();
        for (id, mut sizes) in input.chars().chunks(2).into_iter().enumerate() {
            let file_size: usize = sizes.next().unwrap().to_string().parse().unwrap();
            let blank_size: usize = sizes.next().unwrap_or('0').to_string().parse().unwrap();
            map.extend(vec![Some(id.try_into().unwrap()); file_size]);
            map.extend(vec![None; blank_size]);
        }
        Self(map)
    }

    fn defrag_blocks(&self) -> DiskMap {
        let mut n_file_blocks = 0;
        self.0.iter().for_each(|v| {
            if v.is_some() {
                n_file_blocks += 1
            }
        });
        let mut defragged = self.0.clone();
        let mut rep_index = defragged.len() - 1;
        for i in 0..n_file_blocks {
            let block = defragged.get(i).unwrap();
            if block.is_none() {
                while defragged[rep_index].is_none() {
                    rep_index -= 1;
                }
                defragged.swap(i, rep_index);
            }
            // println!("{}", Self(defragged.clone()));
        }
        defragged.resize(n_file_blocks, None);
        Self(defragged)
    }

    fn defrag_files(&self) -> DiskMap {
        let mut defragged = self.0.clone();
        let max_id = defragged
            .iter()
            .map(|v| v.unwrap_or_default())
            .max()
            .unwrap();

        let mut gaps: Vec<Gap> = Vec::new();
        let mut start = 0;
        while start < defragged.len() {
            if defragged[start].is_none() {
                let mut len = 0;
                while defragged[start + len + 1].is_none() {
                    len += 1;
                }
                len += 1;
                gaps.push(Gap { start, len });
                start += len;
            } else {
                start += 1;
            }
        }

        for id in (0..=max_id).rev() {
            let file_inds: Vec<_> = defragged
                .iter()
                .enumerate()
                .filter(|(_, v)| **v == Some(id))
                .map(|(i, _)| i)
                .collect();
            let file_size = file_inds.len();
            if let Some(gap) = gaps.iter_mut().find(|g| g.len >= file_size) {
                if gap.start <= file_inds[0] {
                    for i in 0..file_size {
                        defragged.swap(gap.start + i, file_inds[0] + i);
                    }
                    gap.start += file_size;
                    gap.len -= file_size;
                }
            }
            // println!("{}", Self(defragged.clone()))
        }
        Self(defragged)
    }

    fn checksum(&self) -> u64 {
        self.0
            .iter()
            .enumerate()
            .map(|(i, v)| i as u64 * v.unwrap_or_default() as u64)
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

fn main() {
    let input = utils::input_lines(9);
    let dm = DiskMap::new(&input);
    let part_1_answer = dm.defrag_blocks().checksum();
    println!("Day 9, Part 1 answer: {}", part_1_answer);
    let part_2_answer = dm.defrag_files().checksum();
    println!("Day 9, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
