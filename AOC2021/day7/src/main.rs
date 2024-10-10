use utils;

fn fuel_to_get_to(starts: &Vec<u64>, target: u64) -> u64 {
    // starts
    //     .into_iter()
    //     .map(|x| (*x as i32 - target as i32).abs())
    //     .sum::<i32>() as u64
    let dists: Vec<_> = starts.iter().map(|x| (*x as i64 - target as i64)).collect();
    let abs_dists: Vec<_> = dists.iter().map(|x| x.abs()).collect();
    let total: i64 = abs_dists.iter().sum();
    if target == 1453 {
        println!("{:#?}", abs_dists)
    }
    total as u64
}

fn minimum_fuel(starts: &Vec<u64>) -> (u64, u64) {
    let positions: Vec<_> =
        (*starts.iter().min().unwrap()..*starts.iter().max().unwrap()).collect();
    // println!("{:?}", positions);
    let fuels: Vec<_> = positions
        .iter()
        .map(|x| fuel_to_get_to(starts, *x))
        .collect();
    positions
        .iter()
        .zip(&fuels)
        .for_each(|x| println!("{:?}", x));
    let (min_pos, min_fuel) = positions
        .into_iter()
        .zip(fuels)
        .min_by(|(_, f1), (_, f2)| f1.cmp(f2))
        .unwrap();
    // let min_pos = (*starts.iter().min().unwrap()..*starts.iter().max().unwrap())
    //     .min_by(|x, y| {
    //         let fx = fuel_to_get_to(starts, *x);
    //         let fy = fuel_to_get_to(starts, *y);
    //         println!("{} -> {}, {} -> {}", *x, fx, *y, fy);
    //         fx.cmp(&fy)
    //     })
    //     .unwrap();
    (min_pos, min_fuel)
}

fn main() {
    let input = utils::input_lines(7);
    let input: Vec<u64> = utils::csv_line(&input[0]).unwrap().into_iter().collect();

    let part_1_answer = minimum_fuel(&input);
    println!("Day 7, Part 1 answer: {:?}", part_1_answer);
}

#[cfg(test)]
mod test;
