use utils;

fn fuel_to_get_to(starts: &Vec<u64>, target: u64) -> u64 {
    starts
        .into_iter()
        .map(|x| (i64::try_from(*x).unwrap() - i64::try_from(target).unwrap()).abs())
        .sum::<i64>() as u64
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
