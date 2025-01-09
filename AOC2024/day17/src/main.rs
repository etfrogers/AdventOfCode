use anyhow::{anyhow, Ok};
use std::{num::ParseIntError, str::FromStr};
use strum_macros::EnumIter;

use utils::{self};

struct Program {
    listing: Vec<Instruction>,
}

type Register = u64;

struct Computer {
    reg_a: Register,
    reg_b: Register,
    reg_c: Register,
    program: Program,
    pointer: usize,
    output_buffer: Vec<u8>,
}

#[repr(u8)]
#[derive(EnumIter, Clone, Copy)]
enum Instruction {
    Adv(ComboOp) = 0,
    Bxl(LiteralOp) = 1,
    Bst(ComboOp) = 2,
    Jnz(LiteralOp) = 3,
    Bxc(LiteralOp) = 4,
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
            Instruction::Bxc(_) => {
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
            0 | 1 | 2 | 3 => val,
            4 => self.reg_a,
            5 => self.reg_b,
            6 => self.reg_c,
            _ => panic!("Invalid combo operand {val}"),
        }
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
            4 => Ok(Instruction::Bxc(operand.into())),
            5 => Ok(Instruction::Out(operand.into())),
            6 => Ok(Instruction::Bdv(operand.into())),
            7 => Ok(Instruction::Cdv(operand.into())),
            _ => Err(anyhow!("Failed to match opcode {opcode}")),
        }
    }
}

fn main() {
    let input = utils::input_lines(17);
    let mut comp = Computer::build(&input);
    let part_1_answer = comp.run();
    println!("Day 17, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
