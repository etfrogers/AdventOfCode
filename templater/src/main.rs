use std::{env, fs, path::Path};

static USAGE: &str = "templater: creates rust template files for Advent of Code

    Usage:
    templater DAY_NUMBER [SUB_DIR]

    DAY_NUMBER is compulsory
    SUB_DIR is optional
    ";
fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 || args.len() > 3 {
        println!("{USAGE}");
        return;
    }
    let day = &args[1];

    println!("templater creating files for day {day}\n");

    let p = String::from("day") + day;
    let dirname = if args.len() == 3 {
        let sub_dir = Path::new(&args[2]);
        if !fs::exists(sub_dir).unwrap() {
            println!("The SUB_DIR directory should be the name of an exsiting directory from the current path");
            println!("\n{USAGE}");
            return;
        } else {
            &sub_dir.join(p)
        }
    } else {
        Path::new(&p)
    };
    let fname = "main.rs";
    let test_name = "test.rs";
    if let Err(err) = fs::create_dir(dirname) {
        if err.raw_os_error().is_some_and(|code| code == 17) {
            println!("Directory {dirname:?} already exists: templater expects to create files for a new day.\n\n{USAGE}");
            return;
        }
        panic!("Failed to create package dir: {err:?}");
    }
    fs::create_dir(dirname.join("src")).expect("Failed to create src dir");

    let toml_code = TOML_TEXT.replace("{#day#}", day);
    let test_code = TEST_TEXT.replace("{#day#}", day);
    let main_code = MAIN_TEXT.replace("{#day#}", day);

    fs::write(dirname.join("src").join(fname), main_code).expect("Failed to write main");
    fs::write(dirname.join("src").join(test_name), test_code).expect("Failed to write test");
    fs::write(dirname.join("Cargo.toml"), toml_code).expect("Failed to write toml");
    fs::write(dirname.join("input.txt"), "").expect("Failed to write input");
}

const MAIN_TEXT: &str = "use utils;

fn main() {
    let input = utils::input_lines({#day#});
    let part_1_answer = 0;
    println!(\"Day {#day#}, Part 1 answer: {}\", part_1_answer);

}

#[cfg(test)]
mod test;

";

const TEST_TEXT: &str = "use rstest::{rstest, fixture};
use super::*;

const TEST_1: &str = \"...\";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}


#[test]
fn test_part1() {
    let input = utils::input_lines({#day#});

    let part_1_answer = 0;
    assert_eq!(part_1_answer, 1);
}
";

const TOML_TEXT: &str = "[package]
name = \"day{#day#}\"
version = \"0.1.0\"
edition = \"2021\"

[dependencies]
utils = { path = \"../../utils\" }

[dev-dependencies]
rstest = \"0.23.0\"
";
