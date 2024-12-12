fn sum_to_n(n: i64) -> i64 {
    n * (n + 1) / 2
}

fn fuel_to_get_to(starts: &[u64], target: u64, extra_fuel: bool) -> u64 {
    let toi = |x: u64| i64::try_from(x).unwrap();
    starts
        .iter()
        .map(|x| {
            let dist = (toi(*x) - toi(target)).abs();
            if extra_fuel {
                sum_to_n(dist)
            } else {
                dist
            }
        })
        .sum::<i64>() as u64
}

fn minimum_fuel(starts: &[u64], extra_fuel: bool) -> (u64, u64) {
    let positions: Vec<_> =
        (*starts.iter().min().unwrap()..*starts.iter().max().unwrap()).collect();
    // println!("{:?}", positions);
    let fuels: Vec<_> = positions
        .iter()
        .map(|x| fuel_to_get_to(starts, *x, extra_fuel))
        .collect();
    // positions
    //     .iter()
    //     .zip(&fuels)
    //     .for_each(|x| println!("{:?}", x));
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

    let part_1_answer = minimum_fuel(&input, false);
    println!("Day 7, Part 1 answer: {:?}", part_1_answer);

    let part_2_answer = minimum_fuel(&input, true);
    println!("Day 7, Part 2 answer: {:?}", part_2_answer);
}

#[cfg(test)]
mod test;
