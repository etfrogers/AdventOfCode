use rustc_hash::FxHashSet;
use utils::{
    self,
    grid::{pos::Coord, Grid, GridFind, GridTrait},
};

struct TopoMap {
    data: Grid<u8>,
}

enum RatingType {
    DistinctRoute,
    EndPoint,
}

impl TopoMap {
    fn new(input: Vec<String>) -> Self {
        Self {
            data: Grid::new_from_strings(input).map(|s| s.to_string().parse().unwrap()),
        }
    }

    fn trailheads(&self) -> impl Iterator<Item = Coord> + '_ {
        self.data.find_all(0)
    }

    fn trailhead_score(&self, trailhead: Coord, rating_type: RatingType) -> usize {
        let mut ends = Vec::<Coord>::new();
        let mut stack = Vec::<Coord>::new();
        let mut visited: FxHashSet<Coord> = FxHashSet::default();
        stack.push(trailhead);
        while let Some(curr) = stack.pop() {
            visited.insert(curr);
            let curr_val = self.data[curr];
            if curr_val == 9 {
                ends.push(curr);
                continue;
            } else {
                for n in self.data.neighbour_coords(&curr, false) {
                    if self.data.is_inside(&n) && self.data[n] == curr_val + 1 {
                        stack.push(n);
                    }
                }
            }
        }
        match rating_type {
            RatingType::EndPoint => FxHashSet::from_iter(ends.iter()).len(),
            RatingType::DistinctRoute => ends.len(),
        }
    }

    fn total_score(&self) -> usize {
        self.trailheads()
            .map(|th| self.trailhead_score(th, RatingType::EndPoint))
            .sum()
    }

    fn total_rating(&self) -> usize {
        self.trailheads()
            .map(|th| self.trailhead_score(th, RatingType::DistinctRoute))
            .sum()
    }
}

fn main() {
    let input = utils::input_lines(10);
    let tm = TopoMap::new(input);
    let part_1_answer = tm.total_score();
    println!("Day 10, Part 1 answer: {}", part_1_answer);

    let part_2_answer = tm.total_rating();
    println!("Day 10, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
