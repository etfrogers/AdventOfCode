use std::{
    collections::{BinaryHeap, HashMap},
    ops::{Deref, DerefMut},
};
use utils::{
    self,
    grid::{Grid, GridFind, GridTrait, direction::Direction, pos::Coord},
};

use crate::MazeSquare::Wall;

#[derive(Copy, Clone, Debug, Eq, PartialEq, Default)]
enum MazeSquare {
    Passage,
    #[default]
    Wall,
    Start,
    End,
}

#[derive(Debug)]
struct Maze {
    data: Grid<MazeSquare>,
}

impl DerefMut for Maze {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.data
    }
}

impl Deref for Maze {
    type Target = Grid<MazeSquare>;

    fn deref(&self) -> &Self::Target {
        &self.data
    }
}

struct Path {
    pos: Coord,
    dir: Direction,
    steps: usize,
    route: Vec<(Coord, Direction)>,
}
impl Eq for Path {}
impl PartialEq for Path {
    fn eq(&self, other: &Self) -> bool {
        self.steps == other.steps
    }
}

impl PartialOrd for Path {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        self.steps.partial_cmp(&other.steps).map(|f| f.reverse())
    }
}
impl Ord for Path {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.steps.cmp(&other.steps).reverse()
    }
}

impl Maze {
    fn new_from_strs(input: Vec<String>) -> Self {
        let data_char = Grid::new_from_strings(input);
        let data: Grid<MazeSquare> = data_char.map(|c| match c {
            '.' => MazeSquare::Passage,
            '#' => MazeSquare::Wall,
            'S' => MazeSquare::Start,
            'E' => MazeSquare::End,
            _ => panic!("Invalid character: {}", c),
        });
        Maze { data }
    }

    fn find_shortest_path(&self) -> usize {
        let start = self.data.find(MazeSquare::Start).unwrap();
        let end = self.data.find(MazeSquare::End).unwrap();
        let mut paths = BinaryHeap::new();
        paths.push(Path {
            pos: start,
            steps: 0,
            dir: Direction::East,
            route: vec![],
        });
        let mut visited: HashMap<(Coord, Direction), usize> = HashMap::new();

        while !paths.is_empty() {
            let Path {
                pos,
                steps,
                dir,
                route,
            } = paths.pop().unwrap();
            if pos == end {
                // println!(
                //     "{}",
                //     visited
                //         .map(|v| match v {
                //             Some(_) => "+",
                //             None => " ",
                //         })
                //         .to_string()
                // );
                return steps;
            }
            if let Some(&best) = visited.get(&(pos, dir)) {
                if steps > best {
                    continue;
                }
            }
            visited.insert((pos, dir), steps);
            for neighbour in self.neighbour_coords(&pos, false) {
                if self[neighbour] == Wall {
                    continue;
                }
                let new_dir = pos.direction_to(&neighbour).unwrap();
                let new_steps = if new_dir == dir {
                    steps + 1
                } else if new_dir == dir.opposite() {
                    continue;
                } else {
                    steps + 1001
                };

                let mut new_route = route.clone();
                new_route.push((neighbour, new_dir));
                paths.push(Path {
                    pos: neighbour,
                    steps: new_steps,
                    dir: new_dir,
                    route: new_route,
                });
            }
        }
        panic!("Failed to find a route")
    }
}

fn main() {
    let input = utils::input_lines(16);
    let maze = Maze::new_from_strs(input);
    let part_1_answer = maze.find_shortest_path();
    println!("Day 16, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
