use std::collections::HashMap;

use petgraph::graph::{NodeIndex, UnGraph};
use utils::{
    self,
    grid::{pos::Coord, Grid},
};

struct Garden(Grid<char>);

struct Region {
    label: char,
    graph: UnGraph<Coord, u8>,
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
                if self.graph.contains_edge(pos_idx, neighbour_idx) {
                    continue;
                }
                self.graph.update_edge(pos_idx, neighbour_idx, 1);
                self.grow(n, neighbour_idx, garden, assigned);
            }
        }
    }

    fn area(&self) -> usize {
        self.graph.node_count()
    }

    fn perimeter(&self) -> usize {
        self.graph
            .node_indices()
            .map(|idx| {
                // println!(
                //     "{:?} -> {:?}: {:?}",
                //     idx,
                //     self.graph.node_weight(idx).unwrap(),
                //     self.graph.neighbors(idx).collect::<Vec<_>>()
                // );
                4 - self
                    .graph
                    .neighbors_undirected(idx)
                    .collect::<Vec<_>>()
                    .len()
            })
            .sum()
    }

    fn cost(&self) -> usize {
        self.area() * self.perimeter()
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
            };
            let pos_idx = region.graph.add_node(pos);
            assigned.insert(pos, pos_idx);

            region.grow(pos, pos_idx, self, &mut assigned);
            regions.push(region);
        }
        regions
    }

    fn total_fencing_cost(&self) -> usize {
        self.regions().iter().map(|r| r.cost()).sum()
    }
}

fn main() {
    let input = utils::input_lines(12);
    let garden = Garden::new(input);
    let part_1_answer = garden.total_fencing_cost();
    println!("Day 12, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
