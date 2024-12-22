use rustc_hash::FxHashSet;
use utils::{
    self,
    grid::{pos::Coord, Grid, GridFind, GridTrait},
};

struct TopoMap {
    data: Grid<u8>,
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

    fn n_routes_from(&self, trailhead: Coord) -> usize {
        let mut ends: FxHashSet<Coord> = FxHashSet::default();
        let mut stack = Vec::<Coord>::new();
        let mut visited: FxHashSet<Coord> = FxHashSet::default();
        stack.push(trailhead);
        while let Some(curr) = stack.pop() {
            visited.insert(curr);
            let curr_val = self.data[curr];
            if curr_val == 9 {
                ends.insert(curr);
                continue;
            } else {
                for n in self.data.neighbour_coords(&curr, false) {
                    if self.data.is_inside(&n) && self.data[n] == curr_val + 1 {
                        stack.push(n);
                    }
                }
            }
        }
        ends.len()
    }

    fn total_routes(&self) -> usize {
        self.trailheads().map(|th| self.n_routes_from(th)).sum()
    }
}

fn main() {
    let input = utils::input_lines(10);
    let tm = TopoMap::new(input);
    let part_1_answer = tm.total_routes();
    println!("Day 10, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
