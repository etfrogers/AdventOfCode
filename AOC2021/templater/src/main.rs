use std::{env, fs, path::Path};

fn main() {
	let args: Vec<String> = env::args().collect();
	if args.len() != 2 {
		println!("templater takes exactly one argument: the day number");
		return
	}
	let day = &args[1];
	println!("templater creating files for day {day}\n");
	// let path = env::current_dir().unwrap();
    // println!("The current directory is {}", path.display());
    
	let p = String::from("day") + day;
	let dirname = Path::new(&p);
	let fname = "main.rs";
	let test_name = "test.rs";
	fs::create_dir(dirname).expect("Failed to create package dir");
	fs::create_dir(dirname.join("src")).expect("Failed to create src dir");

	let toml_code = TOML_TEXT.replace("{#day#}", &day);
	let main_code = MAIN_TEXT.replace("{#day#}", &day);

	fs::write(dirname.join("src").join(fname), main_code).expect("Failed to write main");
	fs::write(dirname.join("src").join(test_name), TEST_TEXT).expect("Failed to write test");
	fs::write(dirname.join("Cargo.toml"), toml_code).expect("Failed to write toml");
	fs::write(dirname.join("input.txt"), "").expect("Failed to write input");
}

const MAIN_TEXT: &str = "use utils;

fn main() {
    let input = utils::input_lines(1{#day#});
    let part_1_answer = 0;
    println!(\"Day {#day#} answer: {}\", part_1_answer);

}

#[cfg(test)]
mod test;

";

const TEST_TEXT: &str = "use super::*;

const TEST_1: &str = \"...\";

#[test]
fn test_part1() {
    let input = utils::input_lines({#day#});
    
    let part1 = 0;
    assert_eq!(part1, 1);
}
";

const TOML_TEXT: &str = "[package]
name = \"day{#day#}\"
version = \"0.1.0\"
edition = \"2021\"

[dependencies]
utils = { path = \"../utils\" }

";
