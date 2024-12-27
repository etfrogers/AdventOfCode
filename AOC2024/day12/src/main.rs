use std::collections::HashMap;

use petgraph::graph::{NodeIndex, UnGraph};
use utils::{
    self,
    grid::{direction::Direction, pos::Coord, Grid},
};

struct Garden(Grid<char>);

struct Region {
    label: char,
    graph: UnGraph<Coord, u8>,
    node_map: HashMap<Coord, NodeIndex>,
}

impl Region {
    fn grow(
        &mut self,
        pos: Coord,
        pos_idx: NodeIndex,
        garden: &Garden,
        assigned: &mut HashMap<Coord, NodeIndex>,
    ) {
        for n in garden.0.neighbour_coords(&pos, false) {
            if garden.0[n] == self.label {
                let neighbour_idx = *assigned.entry(n).or_insert_with(|| self.graph.add_node(n));
                assigned.insert(n, neighbour_idx);
                self.node_map.insert(n, neighbour_idx);
                if self.graph.contains_edge(pos_idx, neighbour_idx) {
                    continue;
                }
                self.graph.update_edge(pos_idx, neighbour_idx, 1);
                self.grow(n, neighbour_idx, garden, assigned);
            }
        }
    }

    pub fn area(&self) -> usize {
        self.graph.node_count()
    }

    pub fn perimeter(&self) -> usize {
        self.graph
            .node_indices()
            .map(|idx| {
                4 - self
                    .graph
                    .neighbors_undirected(idx)
                    .collect::<Vec<_>>()
                    .len()
            })
            .sum()
    }

    pub fn n_sides(&self) -> usize {
        let can_move = |p: Coord, d| {
            if let Ok(trial_pos) = p.add_dir(d) {
                self.node_map.contains_key(&trial_pos)
            } else {
                false
            }
        };

        let mut n = 1;
        let mut pos = self.graph[NodeIndex::new(0)];
        let initial_pos = pos.clone();
        let mut dir = Direction::East;

        // because of the way regions are assigned, this should be the first element
        // on the row, and there should be none in the row above
        assert!(!can_move(pos, dir.left()));
        if !can_move(pos, dir) {
            dir.turn_right();
            n += 1;
        }
        let initial_dir = dir;
        // println!("Initial: {initial_pos}, {initial_dir}, {n}");
        loop {
            // println!("{pos}, {dir}, {n}");
            pos.move_(dir);

            if can_move(pos, dir.left()) {
                // Left
                dir.turn_left();
                n += 1;
            } else if can_move(pos, dir) {
                // Straight on
                // do nothing
            } else if can_move(pos, dir.right()) {
                // Right
                dir.turn_right();
                n += 1;
            } else {
                // go back
                dir.turn_right();
                dir.turn_right();
                n += 2;
            }

            if pos == initial_pos {
                // println!("At start {pos}, {dir}, {n}");
                if dir == initial_dir {
                    break;
                }
            }
        }
        if initial_dir == Direction::South {
            n - 2
        } else {
            n - 1
        }
    }

    pub fn cost(&self, with_discount: bool) -> usize {
        self.area()
            * if with_discount {
                self.n_sides()
            } else {
                self.perimeter()
            }
    }
}

impl Garden {
    fn new(input: Vec<String>) -> Self {
        Self(Grid::new_from_strings(input))
    }

    fn regions(&self) -> Vec<Region> {
        let mut assigned = HashMap::new();
        let mut regions = Vec::new();
        for pos in self.0.coords() {
            if assigned.contains_key(&pos) {
                continue;
            }
            let mut region = Region {
                graph: UnGraph::new_undirected(),
                label: self.0[pos],
                node_map: HashMap::new(),
            };
            let pos_idx = region.graph.add_node(pos);
            assigned.insert(pos, pos_idx);

            region.grow(pos, pos_idx, self, &mut assigned);
            regions.push(region);
        }
        regions
    }

    fn total_fencing_cost(&self, with_discount: bool) -> usize {
        self.regions().iter().map(|r| r.cost(with_discount)).sum()
    }
}

fn main() {
    let input = utils::input_lines(12);
    let garden = Garden::new(input);
    let part_1_answer = garden.total_fencing_cost(false);
    println!("Day 12, Part 1 answer: {}", part_1_answer);

    let part_2_answer = garden.total_fencing_cost(true);
    println!("Day 12, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
