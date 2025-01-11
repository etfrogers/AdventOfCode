use anyhow::{anyhow, Ok};
use std::str::FromStr;
use strum_macros::EnumIter;

const DEBUG: bool = false;

macro_rules! debug_println {
    ($($arg:tt)*) => {
        if DEBUG {
            println!($($arg)*)
        }
    };
}
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

    fn find_quine(&self) -> Register {
        self.program.find_quine()
    }

    #[allow(dead_code)]
    fn find_quine_brute_force(&mut self) -> Register {
        for candidate in 0.. {
            if candidate % 1000 == 0 {
                debug_println!("{candidate}")
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

impl Program {
    fn find_quine(&self) -> Register {
        let original_program: Vec<_> = self.original_listing.iter().map(|v| (*v).into()).collect();
        *invert_prog(&original_program).iter().min().unwrap()
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
    loop {
        // Bst(ComboOp(4))
        debug_println!("\n loop start: \n\ta: {a:b} ({a})");
        let mut b = a % 8; // b = Lowest three bits of a
                           // Bxl(LiteralOp(2))
                           // debug_println!("b: {b:b}");
        b ^= 2;
        debug_println!("b: {b:b} ({b})");
        // Cdv(ComboOp(5))
        // c = a / 2_u64.pow(b.try_into().unwrap());
        // Bxc
        // b ^= c;
        // b ^= a / 2_u64.pow(b.try_into().unwrap());
        debug_println!("a >> b: {:b}", a >> b);
        b ^= a >> b; // last 3 bits of b xor'ed with digits b-(b+3) of a
                     // debug_println!("b: {b:b}");
                     // Adv(ComboOp(3))
                     // a = a / 2 ^ 3;
                     // Bxl(LiteralOp(7))
        b ^= 7;
        debug_println!("b: {b:b}");
        // Out(ComboOp(5))
        output.push(b % 8);
        debug_println!(
            "output: {} - {:b}",
            output[output.len() - 1],
            output[output.len() - 1]
        );
        // Jnz(LiteralOp(0))
        // a /= 8;
        a >>= 3;
        debug_println!("a: {a:b}");

        if a == 0 {
            break;
        }
    }
    output
}

#[derive(Debug)]
struct SearchPoint<'a> {
    a: Register,
    remaining_input: &'a [Register],
    input_so_far: Vec<Register>,
}

fn invert_prog(output: &[Register]) -> Vec<Register> {
    let a = 0;
    let input: Vec<_> = output.iter().rev().copied().collect();
    let initial_point = SearchPoint {
        a,
        remaining_input: &input[..],
        input_so_far: Vec::new(),
    };
    let mut search_stack = Vec::new();
    search_stack.push(initial_point);
    let mut poss_answers = Vec::new();
    while let Some(search) = search_stack.pop() {
        if search.remaining_input.is_empty() {
            poss_answers.push(search.a);
            debug_println!("Saving output: {}", search.a);
            continue;
        }
        let mut b = search.remaining_input[0];
        let a = search.a;
        debug_println!("\ncurrent a: {a:b}\nb input: {b:b}");
        b ^= 7;
        debug_println!("b: {b:b}");
        for c in 0..=7 {
            debug_println!("c: {c}");
            let poss_a = (a << 3) | c;
            let shift = c ^ 2;
            debug_println!(
                "poss_a: {poss_a:b}, shift: {shift}, (poss_a >> shift), {:b}, (shift ^ (poss_a >> shift)) % 8: {:b}",
                poss_a >> shift,
                (shift ^ (poss_a >> shift)) % 8
            );
            if (shift ^ (poss_a >> shift)) % 8 == b {
                debug_println!("---Found\n");

                let mut new_so_far = search.input_so_far.clone();
                new_so_far.insert(0, search.remaining_input[0]);
                debug_println!(
                    "Poss_a: {poss_a}, output of poss_a: {:?}, expected_output: {new_so_far:?}",
                    translated_prog(poss_a)
                );
                if translated_prog(poss_a) == new_so_far {
                    let new_point = SearchPoint {
                        a: poss_a,
                        remaining_input: &search.remaining_input[1..],
                        input_so_far: new_so_far,
                    };
                    debug_println!("pushing: {new_point:?}");
                    search_stack.push(new_point);
                } else {
                    debug_println!("Pruning search")
                }
            };
        }
    }
    debug_println!("{poss_answers:?}");
    poss_answers
}

fn main() {
    let input = utils::input_lines(17);
    let mut comp = Computer::build(&input);
    let part_1_answer = comp.run();
    println!("Day 17, Part 1 answer: {}", part_1_answer);

    let part_2_answer = comp.find_quine();
    println!("{:?}", translated_prog(part_2_answer));
    println!("Day 17, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
