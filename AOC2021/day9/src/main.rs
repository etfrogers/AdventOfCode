use utils::{self, grid::Grid};

struct HeightMap {
    data: Grid<u32>,
}

impl HeightMap {
    fn build(input: Vec<String>) -> Self {
        Self {
            data: Grid::new_from_strings(input).map(|s| String::from(*s).parse().unwrap()),
        }
    }

    fn low_points(&self) -> impl Iterator<Item = u32> + '_ {
        self.data
            .coord_iter(false, false)
            .filter(|c| {
                let lp_value = self.data.get_c(c);
                self.data.neighbours(&c).all(|v| v > lp_value)
            })
            .map(|c| self.data.get_c(&c))
            .copied()
    }

    fn risk_levels(&self) -> impl Iterator<Item = u32> + '_ {
        self.low_points().map(|v| v + 1)
    }

    fn total_risk(&self) -> u32 {
        self.risk_levels().sum()
    }
}

fn main() {
    let input = utils::input_lines(9);
    let hm = HeightMap::build(input);
    let part_1_answer = hm.total_risk();
    println!("Day 9, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
