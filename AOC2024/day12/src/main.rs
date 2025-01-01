use std::collections::{HashMap, HashSet};

use itertools::izip;
use petgraph::graph::{NodeIndex, UnGraph};
use utils::{
    self,
    grid::{
        direction::{Direction, DIAGONAL_MOVES},
        pos::Coord,
        Grid,
    },
};

struct Garden(Grid<char>);

#[derive(Debug)]
struct Region {
    label: char,
    graph: UnGraph<Coord, u8>,
    node_map: HashMap<Coord, NodeIndex>,
    n_sides: usize,
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
        self.graph
            .node_indices()
            .map(|idx| {
                let pos = self.graph.node_weight(idx).unwrap();
                let ortho_neighbours: Vec<Direction> = self
                    .graph
                    .neighbors_undirected(idx)
                    .map(|i| {
                        let n = *self.graph.node_weight(i).unwrap();
                        pos.direction_to(&n).unwrap()
                    })
                    .collect();

                let diag_neighbours: Vec<_> = DIAGONAL_MOVES
                    .keys()
                    .filter(|dir| {
                        pos.add_dir(**dir)
                            .ok()
                            .filter(|p| self.node_map.contains_key(&p))
                            .is_some()
                    })
                    .copied()
                    .collect();
                let n_ortho = ortho_neighbours.len();
                let n_diag = diag_neighbours.len();
                let n = match n_ortho {
                    0 => {
                        // ?.?
                        // .O.
                        // ?.?
                        // as long as the four ortho neighbours are not filled, then this is a dot with four sides
                        4
                    }
                    1 => {
                        2
                        // let orth = ortho_neighbours[0];
                        // let n_adj = diag_neighbours
                        //     .iter()
                        //     .filter(|d| orth.is_adjacent(d))
                        //     .collect::<Vec<_>>()
                        //     .len();
                        // if n_adj == 0 {
                        //     // .X.
                        //     // .O.
                        //     // ?.?
                        //     2
                        // } else {
                        //     // ?X?
                        //     // .O.
                        //     // ?.?
                        //     // the one above is an inner corner
                        //     1
                        // }
                    }
                    2 => {
                        let n1 = ortho_neighbours[0];
                        let n2 = ortho_neighbours[1];
                        if n1.is_opposite(&n2) {
                            // ?X?
                            // .O.
                            // ?X?
                            if n_diag == 0 {
                                // .X.
                                // .O.
                                // .X.
                                0
                            } else {
                                // think the ones above and below being inner corners will handle this
                                0
                            }
                        } else {
                            debug_assert!(n1.is_right_angles(&n2));
                            // ?X?
                            // .OX
                            // ?.?
                            if diag_neighbours.contains(&n1.direction_between(&n2).unwrap()) {
                                //Outer corner only
                                1
                            } else {
                                // inner AND outer corner
                                2
                            }
                        }
                    }
                    3 => {
                        // ?X?
                        // XOX
                        // ?.?
                        let mut centre = None;
                        for i in 0..3 {
                            let test = ortho_neighbours[i];
                            let other1 = ortho_neighbours[(i + 1) % 3];
                            let other2 = ortho_neighbours[(i + 2) % 3];

                            if test.is_right_angles(&other1) && test.is_right_angles(&other2) {
                                centre = Some(test);
                            }
                        }
                        let centre = centre.unwrap();
                        let n_adj = diag_neighbours
                            .iter()
                            .filter(|d| centre.is_adjacent(d))
                            .collect::<Vec<_>>()
                            .len();
                        // if n_adj == 0 {
                        //     // .X.
                        //     // XOX
                        //     // ...
                        //     2
                        // }else if {
                        //     // .XX
                        //     // XOX
                        //     // ...
                        //     1

                        //     // case where botom diags are occupied is dealt with by left/right square:
                        //     // e.g.
                        //     // .X.
                        //     // XOX
                        //     // ..X
                        // }
                        2 - n_adj
                        // } else {
                        //     0
                    }
                    4 => {
                        // if n_diag == 4 {
                        //Centre
                        // 0
                        // } else {
                        4 - n_diag
                        // }
                    }
                    _ => panic!("Unhandled case: "),
                };
                println!("{pos}:\t{ortho_neighbours:?}\t{diag_neighbours:?}\t{n}");
                n
            })
            .sum()
    }

    fn n_outer_sides(&self) -> usize {
        let can_move = |p: Coord, d| {
            if let Ok(trial_pos) = p.add_dir(d) {
                self.node_map.contains_key(&trial_pos)
            } else {
                false
            }
        };

        let mut n = 1;
        let mut pos = self.graph[NodeIndex::new(0)];
        let initial_pos = pos;
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
                n_sides: 0,
            };
            let pos_idx = region.graph.add_node(pos);
            assigned.insert(pos, pos_idx);

            region.grow(pos, pos_idx, self, &mut assigned);
            regions.push(region);
        }

        let encloses = self.find_enclosures(&regions);
        let outer_sides: Vec<_> = regions.iter().map(|r| r.n_outer_sides()).collect();
        for (region, enc, n_outer) in izip!(regions.iter_mut(), encloses, outer_sides.iter()) {
            region.n_sides = n_outer + enc.iter().map(|idx| outer_sides[*idx]).sum::<usize>();
        }

        regions
    }

    fn find_enclosures(&self, regions: &[Region]) -> Vec<Vec<usize>> {
        let regions_sets: Vec<HashSet<Coord>> = regions
            .iter()
            .map(|r| HashSet::from_iter(r.graph.node_weights().copied()))
            .collect::<Vec<_>>();
        let enclosed_by: Vec<_> = regions
            .iter()
            .enumerate()
            .map(|(self_index, region)| {
                let mut enclosure = None;
                for pos in region.graph.node_weights() {
                    if self.0.is_edge(pos) {
                        return None;
                    }
                    for n in self.0.neighbour_coords(pos, false) {
                        let candidate = regions_sets.iter().position(|s| s.contains(&n)).unwrap();
                        // let candidate = &regions[index];
                        if candidate == self_index {
                            continue;
                        }
                        match enclosure {
                            None => enclosure = Some(candidate),
                            Some(cand) => {
                                if cand != candidate {
                                    return None;
                                }
                            }
                        }
                    }
                }
                enclosure
            })
            .collect();
        let mut encloses = vec![Vec::new(); regions.len()];
        for (idx, enc_by) in enclosed_by.iter().enumerate() {
            if let Some(enc_idx) = enc_by {
                encloses[*enc_idx].push(idx)
            }
        }
        encloses
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
