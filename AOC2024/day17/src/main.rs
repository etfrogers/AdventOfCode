use anyhow::{anyhow, Ok};
use std::str::FromStr;
use strum_macros::EnumIter;

use utils::{self};

#[derive(Debug)]
struct Program {
    listing: Vec<Instruction>,
    original_listing: Vec<u8>,
}

type Register = u64;

#[derive(Debug)]
struct Computer {
    reg_a: Register,
    reg_b: Register,
    reg_c: Register,
    program: Program,
    pointer: usize,
    output_buffer: Vec<u8>,
}

#[repr(u8)]
#[derive(Debug, EnumIter, Clone, Copy)]
enum Instruction {
    Adv(ComboOp) = 0,
    Bxl(LiteralOp) = 1,
    Bst(ComboOp) = 2,
    Jnz(LiteralOp) = 3,
    Bxc = 4,
    Out(ComboOp) = 5,
    Bdv(ComboOp) = 6,
    Cdv(ComboOp) = 7,
}

#[derive(Debug, Default, Clone, Copy)]
struct ComboOp(Register);

#[derive(Debug, Default, Clone, Copy)]
struct LiteralOp(Register);

impl Computer {
    fn build(input: &[String]) -> Self {
        let reg_a = Computer::parse_reg_line(&input[0]);
        let reg_b = Computer::parse_reg_line(&input[1]);
        let reg_c = Computer::parse_reg_line(&input[2]);
        assert!(input[3].is_empty());
        let program = Program::from_str(&input[4]).unwrap();

        Computer {
            reg_a,
            reg_b,
            reg_c,
            program,
            pointer: 0,
            output_buffer: Vec::new(),
            // original_listing: input[4].split(": ").last().unwrap().to_string(),
        }
    }

    fn parse_reg_line(line: &str) -> Register {
        line.split(": ").last().unwrap().parse().unwrap()
    }

    fn run(&mut self) -> String {
        while self.pointer < self.program.listing.len() {
            if self.apply(self.program.listing[self.pointer]) {
                self.pointer += 1
            }
        }
        self.output_buffer
            .iter()
            .map(|v| format!("{v}"))
            .collect::<Vec<_>>()
            .join(",")
    }

    fn apply(&mut self, instruction: Instruction) -> bool {
        let div = |op| self.reg_a / 2_u64.pow(self.combo_value(op).try_into().unwrap());
        match instruction {
            Instruction::Adv(op) => {
                self.reg_a = div(op);
                true
            }
            Instruction::Bxl(op) => {
                self.reg_b ^= op.0;
                true
            }
            Instruction::Bst(op) => {
                self.reg_b = self.combo_value(op) % 8;
                true
            }
            Instruction::Jnz(op) => {
                if self.reg_a != 0 {
                    self.pointer = op.0.try_into().unwrap();
                    false
                } else {
                    true
                }
            }
            Instruction::Bxc => {
                self.reg_b ^= self.reg_c;
                true
            }
            Instruction::Out(op) => {
                self.output_buffer
                    .push((self.combo_value(op) % 8).try_into().unwrap());
                true
            }
            Instruction::Bdv(op) => {
                self.reg_b = div(op);
                true
            }
            Instruction::Cdv(op) => {
                self.reg_c = div(op);
                true
            }
        }
    }

    fn combo_value(&self, value: ComboOp) -> Register {
        let val = value.0;
        match val {
            0..=3 => val,
            4 => self.reg_a,
            5 => self.reg_b,
            6 => self.reg_c,
            _ => panic!("Invalid combo operand {val}"),
        }
    }

    fn find_quine(&mut self) -> Register {
        for candidate in 0.. {
            if candidate % 1000 == 0 {
                println!("{candidate}")
            }
            self.reset();
            self.reg_a = candidate;
            self.run();
            if self.output_buffer == self.program.original_listing {
                return candidate;
            }
        }
        panic!("Failed to converge");
    }

    fn reset(&mut self) {
        self.reg_a = 0;
        self.reg_b = 0;
        self.reg_c = 0;
        self.pointer = 0;
        self.output_buffer = Vec::new();
    }
}

impl FromStr for Program {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let listing: Vec<u8> = s
            .split(": ")
            .last()
            .ok_or_else(|| anyhow!("Failed to parse {s}"))?
            .split(",")
            .map(|s| s.parse::<u8>().map_err(|e| anyhow!(e)))
            .collect::<Result<Vec<u8>, anyhow::Error>>()?;

        Ok(Self {
            listing: listing
                .chunks(2)
                .map(|pair| Instruction::new(pair[0], pair[1].into()))
                .collect::<anyhow::Result<Vec<_>>>()?,
            original_listing: listing,
        })
    }
}

impl From<Register> for LiteralOp {
    fn from(value: Register) -> Self {
        Self(value)
    }
}

impl From<Register> for ComboOp {
    fn from(value: Register) -> Self {
        Self(value)
    }
}

impl Instruction {
    fn new(opcode: u8, operand: Register) -> anyhow::Result<Self> {
        match opcode {
            0 => Ok(Instruction::Adv(operand.into())),
            1 => Ok(Instruction::Bxl(operand.into())),
            2 => Ok(Instruction::Bst(operand.into())),
            3 => Ok(Instruction::Jnz(operand.into())),
            4 => Ok(Instruction::Bxc),
            5 => Ok(Instruction::Out(operand.into())),
            6 => Ok(Instruction::Bdv(operand.into())),
            7 => Ok(Instruction::Cdv(operand.into())),
            _ => Err(anyhow!("Failed to match opcode {opcode}")),
        }
    }
}

fn translated_prog(mut a: Register) -> Vec<Register> {
    let mut output: Vec<Register> = Vec::new();
    // let mut a: Register = 0;

    // let mut c;
    loop {
        // Bst(ComboOp(4))
        println!("\n loop start: \n\ta: {a:b} ({a})");
        let mut b = a % 8; // b = Lowest three bits of a
                           // Bxl(LiteralOp(2))
        println!("b: {b:b}");
        b ^= 2;
        println!("b: {b:b} ({b})");
        // Cdv(ComboOp(5))
        // c = a / 2_u64.pow(b.try_into().unwrap());
        // Bxc
        // b ^= c;
        // b ^= a / 2_u64.pow(b.try_into().unwrap());
        println!("a >> b: {:b}", a >> b);
        b ^= a >> b; // last 3 bits of b xor'ed with digits b-(b+3) of a
        println!("b: {b:b}");
        // Adv(ComboOp(3))
        // a = a / 2 ^ 3;
        // Bxl(LiteralOp(7))
        b ^= 7;
        println!("b: {b:b}");
        // Out(ComboOp(5))
        output.push(b % 8);
        println!(
            "output: {} - {:b}",
            output[output.len() - 1],
            output[output.len() - 1]
        );
        // Jnz(LiteralOp(0))
        // a /= 8;
        a = a >> 3;
        println!("a: {a:b}");

        if a == 0 {
            break;
        }
    }
    output
}

fn invert_prog(output: Vec<Register>) -> Register {
    let mut a = 0;
    let mut input: Vec<_> = output.iter().rev().collect();
    'input_loop: while let Some(b) = input.pop() {
        let mut b = *b;
        println!("\ncurrent a: {a:b}\nb input: {b:b}");
        b ^= 7;
        println!("b: {b:b}");
        // let mut shift = None;
        let mut new_a = 0;
        for c in 0..=7 {
            // println!("a << c: {:b}", a << 3);
            println!("c: {c}");
            // println!("a << c | c: {:b}", (a << 3) | c);
            let poss_a = (a << 3) | c;
            let shift = c ^ 2;
            println!(
                "poss_a: {poss_a:b}, shift: {shift}, (poss_a >> shift), {:b}, (shift ^ (poss_a >> shift)) % 8: {:b}",
                poss_a >> shift,
                (shift ^ (poss_a >> shift)) % 8
            );
            if (shift ^ (poss_a >> shift)) % 8 == b {
                println!("---Found\n");
                // shift = Some(c);
                new_a = poss_a;
                // break;
            };
            // if poss_a >> c == b {
            //     a = poss_a;
            //     break;
            // }
        }
        a = new_a;
        // let shift = shift.unwrap();
        // b ^= a >> shift;
        // println!("b: {b:b}");
        // b ^= 2;
        // println!("b: {b:b}");
        // a = a << 3 | b % 8;
        // println!("a: {a:b}\n");
    }
    a
}

fn find_quine_translated() -> u64 {
    let orig_prog = vec![2, 4, 1, 2, 7, 5, 4, 5, 0, 3, 1, 7, 5, 5, 3, 0];
    for candidate in 0.. {
        if candidate % 1000000 == 0 {
            println!("{candidate}")
        }

        if translated_prog(candidate) == orig_prog {
            return candidate;
        }
    }
    panic!("Failed to converge");
}

fn main() {
    let input = utils::input_lines(17);
    let mut comp = Computer::build(&input);
    let part_1_answer = comp.run();
    println!("Day 17, Part 1 answer: {}", part_1_answer);

    // let mut comp = Computer::build(&input);
    // println!("{comp:?}");
    let part_2_answer = find_quine_translated();
    println!("{:?}", translated_prog(part_2_answer));
    println!("Day 17, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
