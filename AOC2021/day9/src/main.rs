use std::{collections::HashSet, ops::Deref};

use utils::{
    self,
    grid::{pos::Coord, Grid, GridTrait},
};

struct HeightMap {
    data: Grid<u32>,
}

impl Deref for HeightMap {
    type Target = Grid<u32>;

    fn deref(&self) -> &Self::Target {
        &self.data
    }
}

impl HeightMap {
    fn build(input: Vec<String>) -> Self {
        Self {
            data: Grid::new_from_strings(input).map(|s| String::from(*s).parse().unwrap()),
        }
    }

    fn low_point_coords(&self) -> impl Iterator<Item = Coord> + '_ {
        self.coords().filter(|c| {
            let lp_value = self[*c];
            self.neighbours(c, false).all(|v| *v > lp_value)
        })
    }

    fn low_points(&self) -> impl Iterator<Item = u32> + '_ {
        self.low_point_coords().map(|c| self[c])
    }

    fn risk_levels(&self) -> impl Iterator<Item = u32> + '_ {
        self.low_points().map(|v| v + 1)
    }

    fn total_risk(&self) -> u32 {
        self.risk_levels().sum()
    }

    fn basins(&self) -> impl Iterator<Item = u32> + '_ {
        self.low_point_coords().map(|c| {
            let mut to_visit = vec![c];
            let mut members = HashSet::<Coord>::from([c]);
            while to_visit.len() > 0 {
                let coord = to_visit.pop().unwrap();
                members.insert(coord);
                for pos in self.neighbour_coords(&coord, false) {
                    let candidate = Coord::try_from(pos).unwrap();
                    if !members.contains(&candidate) && self[candidate] < 9 {
                        to_visit.push(candidate);
                    }
                }
            }
            members.len().try_into().unwrap()
        })
    }

    fn basin_checksum(&self) -> u32 {
        let mut sizes: Vec<_> = self.basins().collect();
        sizes.sort();
        sizes[sizes.len() - 3..].iter().product()
    }
}

fn main() {
    let input = utils::input_lines(9);
    let hm = HeightMap::build(input);
    let part_1_answer = hm.total_risk();
    println!("Day 9, Part 1 answer: {}", part_1_answer);
    let part_2_answer = hm.basin_checksum();
    println!("Day 9, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
