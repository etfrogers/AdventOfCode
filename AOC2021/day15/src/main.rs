use std::{collections::BinaryHeap, usize};

use utils::{
    self,
    grid::{pos::Coord, Grid, GridTrait},
};

struct RiskLevel {
    map: Grid<usize>,
}

#[derive(Debug, Clone)]
struct Path {
    total_risk: usize,
    route: Vec<Coord>,
}

impl Path {
    fn current_pos(&self) -> &Coord {
        self.route.last().unwrap()
    }
}

impl PartialEq for Path {
    fn eq(&self, other: &Self) -> bool {
        self.total_risk == other.total_risk //&& self.route == other.route
    }
}

impl Eq for Path {}

impl PartialOrd for Path {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        other.total_risk.partial_cmp(&self.total_risk)
        // match self.total_risk.partial_cmp(&other.total_risk) {
        //     Some(core::cmp::Ordering::Equal) => {}
        //     ord => return ord,
        // }
        // self.route.partial_cmp(&other.route)
    }
}

impl Ord for Path {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        other.total_risk.cmp(&self.total_risk)
    }
}

impl RiskLevel {
    fn build(input: Vec<String>) -> Self {
        Self {
            map: Grid::new_from_strings(input).map(|s| String::from(*s).parse().unwrap()),
        }
    }

    fn find_lowest_risk_path(&self) -> Option<Path> {
        let mut paths = BinaryHeap::new();
        let mut shortest_path_to = Grid::full(self.map.n_cols(), self.map.n_rows(), usize::MAX);
        let start = Coord::new(0, 0);
        paths.push(Path {
            total_risk: 0,
            route: vec![start],
        });
        shortest_path_to[start] = 0;
        while paths.len() > 0 {
            let curr_path = paths.pop().unwrap();
            let curr_pos = curr_path.current_pos();
            if curr_path.total_risk > shortest_path_to[*curr_pos] {
                continue;
            }
            for n in self.map.neighbour_coords(curr_pos, false) {
                let mut new_path = curr_path.clone();
                if new_path.route.contains(&n) {
                    continue;
                }
                new_path.total_risk += self.map[n];
                new_path.route.push(n.clone());
                if n.y() == self.map.n_rows() - 1 && n.x() == self.map.n_cols() - 1 {
                    return Some(new_path);
                } else {
                    if new_path.total_risk < shortest_path_to[n] {
                        shortest_path_to[n] = new_path.total_risk;
                        paths.push(new_path);
                    }
                }
            }
        }
        None
    }
}

fn main() {
    let input = utils::input_lines(15);
    let rl = RiskLevel::build(input);
    let path = rl.find_lowest_risk_path().unwrap();
    let part_1_answer = path.total_risk;
    println!("Day 15, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
