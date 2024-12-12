#![allow(dead_code)]
use std::{cell::RefCell, collections::VecDeque};
use utils::{input_lines, StringParseError};

type Register = RefCell<NumberType>;
type NumberType = i128;

#[allow(dead_code)]
mod prog;

struct Alu {
    w: Register,
    x: Register,
    y: Register,
    z: Register,
}

impl Alu {
    fn new() -> Self {
        // let init = || RefCell::new(BigInt::from(0));
        let init = || RefCell::new(0);
        Alu {
            w: init(),
            x: init(),
            y: init(),
            z: init(),
        }
    }

    fn get_register<'a>(&'a self, name: Option<&str>) -> Option<Arg<'a>> {
        match name {
            Some(name) => {
                let reg = match name {
                    "w" => &self.w,
                    "x" => &self.x,
                    "y" => &self.y,
                    "z" => &self.z,
                    r => {
                        let val = r
                            .parse()
                            .unwrap_or_else(|_| panic!("Unexpected register: {}", r));
                        return Some(Arg {
                            ptr: None,
                            data: Some(val),
                        });
                    }
                };
                Some(Arg {
                    ptr: Some(reg),
                    data: None,
                })
            }
            None => None,
        }
    }
}

struct Program<'a> {
    listing: Vec<Instruction<'a>>,
}

#[derive(Debug)]
struct Arg<'a> {
    data: Option<NumberType>,
    ptr: Option<&'a Register>,
}

impl<'a> Arg<'a> {
    fn check_validity(&self) {
        assert!(
            (self.data.is_some() & self.ptr.is_none()) ^ (self.data.is_none() & self.ptr.is_some())
        )
    }
}

impl<'a> Arg<'a> {
    fn get(&self) -> NumberType {
        self.check_validity();
        if self.ptr.is_some() {
            *self.ptr.unwrap().borrow()
        } else {
            self.data.unwrap()
        }
    }

    fn set(&self, value: NumberType) {
        self.check_validity();
        if self.ptr.is_some() {
            *self.ptr.unwrap().borrow_mut() = value;
        } else {
            panic!("Cannot set a number-based Arg")
        }
    }
}

#[derive(Debug)]
enum Instruction<'a> {
    Input(Arg<'a>),
    Add(Arg<'a>, Arg<'a>),
    Multiply(Arg<'a>, Arg<'a>),
    Divide(Arg<'a>, Arg<'a>),
    Modulo(Arg<'a>, Arg<'a>),
    Equal(Arg<'a>, Arg<'a>),
}

impl<'a> Instruction<'a> {
    fn from_str(s: &str, alu: &'a Alu) -> Result<Self, StringParseError> {
        let mut tokens = s.split_ascii_whitespace();
        let command = tokens.next().ok_or_else(|| StringParseError::new(s))?;
        let arg1 = tokens.next().ok_or_else(|| StringParseError::new(s))?;
        let arg2 = tokens.next();

        let arg1 = alu.get_register(Some(arg1)).unwrap();
        let arg2 = alu.get_register(arg2);

        let inst = match command {
            "inp" => {
                assert!(arg2.is_none());
                Instruction::Input(arg1)
            }
            "add" => Instruction::Add(arg1, arg2.unwrap()),
            "mul" => Instruction::Multiply(arg1, arg2.unwrap()),
            "div" => Instruction::Divide(arg1, arg2.unwrap()),
            "mod" => Instruction::Modulo(arg1, arg2.unwrap()),
            "eql" => Instruction::Equal(arg1, arg2.unwrap()),
            cmd => panic!("unexpected command {}", cmd),
        };
        Ok(inst)
    }
}

impl<'a> Program<'a> {
    fn build(input: Vec<String>, alu: &'a Alu) -> Self {
        Self {
            listing: input
                .into_iter()
                .map(|s| Instruction::from_str(&s, alu).unwrap())
                .collect(),
        }
    }

    fn run(&self, input: Vec<NumberType>) {
        let mut input = VecDeque::from(input);
        for inst in &self.listing {
            if DEBUG {
                // println!("{:?}", inst)
            }
            match inst {
                Instruction::Input(reg) => reg.set(input.pop_front().expect("Too few inputs")),
                Instruction::Add(reg, arg) => reg.set(reg.get() + arg.get()),
                Instruction::Multiply(reg, arg) => reg.set(reg.get() * arg.get()),
                Instruction::Divide(reg, arg) => reg.set(reg.get() / arg.get()),
                Instruction::Modulo(reg, arg) => reg.set(reg.get() % arg.get()),
                Instruction::Equal(reg, arg) => {
                    reg.set(Into::<NumberType>::into(reg.get() == arg.get()))
                }
            }
        }
    }
}

const DEBUG: bool = true;

fn main() {
    let program = input_lines(24);
    let alu = Alu::new();
    let _program = Program::build(program, &alu);
    let mut input: Vec<i128> = vec![9; 14];
    input[13] = 10; // for first decrement to work
    let mut _j = 0;

    loop {
        // j += 1;
        // let mut i = 13;
        // loop {
        //     input[i] -= 1;
        //     if input[i] > 0 {
        //         break;
        //     } else {
        //         input[i] = 9;
        //         i -= 1;
        //     }
        // }
        // if DEBUG && j % 10000000 == 0 {
        //     println!("{:?}", input);
        // }
        if prog::program3(&input) {
            break;
        }
        // if *alu.z.borrow() == BigInt::from(0) {
        //     break;
        // }
    }

    let part_1_answer = input;
    println!("Day 24, Part 1 answer: {:?}", part_1_answer);
}

#[cfg(test)]
mod test;
