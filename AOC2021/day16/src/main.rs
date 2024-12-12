use std::{collections::HashMap, str::FromStr};

use lazy_static::lazy_static;
use utils::StringParseError;

lazy_static! {
    static ref DECODE: HashMap<char, Vec<u8>> = HashMap::from([
        ('0', vec![0, 0, 0, 0]),
        ('1', vec![0, 0, 0, 1]),
        ('2', vec![0, 0, 1, 0]),
        ('3', vec![0, 0, 1, 1]),
        ('4', vec![0, 1, 0, 0]),
        ('5', vec![0, 1, 0, 1]),
        ('6', vec![0, 1, 1, 0]),
        ('7', vec![0, 1, 1, 1]),
        ('8', vec![1, 0, 0, 0]),
        ('9', vec![1, 0, 0, 1]),
        ('A', vec![1, 0, 1, 0]),
        ('B', vec![1, 0, 1, 1]),
        ('C', vec![1, 1, 0, 0]),
        ('D', vec![1, 1, 0, 1]),
        ('E', vec![1, 1, 1, 0]),
        ('F', vec![1, 1, 1, 1]),
    ]);
}

#[derive(Debug, PartialEq, Eq)]
struct Packet {
    version: u64,
    type_id: u64,
    content: PacketContent,
}

#[derive(Debug, PartialEq, Eq)]
enum PacketContent {
    Literal(u64),
    Operator {
        length_type: LengthType,
        subpackets: Vec<Packet>,
    },
}

#[derive(Debug, PartialEq, Eq)]
enum LengthType {
    TotalLength(usize),
    NPackets(usize),
}

fn expand_hex(str: &str) -> Vec<u8> {
    let mut output = Vec::with_capacity(str.len() * 4);
    for c in str.chars() {
        output.extend(DECODE[&c].iter());
    }
    output
}

fn parse_int(data: &[u8], start: usize, len: usize) -> (u64, usize) {
    let mut output: u64 = 0;
    for (i, ind) in (start..start + len).rev().enumerate() {
        output += 2_u64.pow(i.try_into().unwrap()) * Into::<u64>::into(data[ind]);
    }
    (output, start + len)
}

fn parse_literal(data: &[u8], start: usize) -> (u64, usize) {
    let mut ptr = start;
    let mut bits: Vec<u8> = Vec::new();
    loop {
        let header_bit: u8 = data[ptr];
        bits.extend_from_slice(&data[ptr + 1..ptr + 5]);
        ptr += 5;
        if header_bit == 0 {
            break;
        }
    }
    let (value, _) = parse_int(&bits, 0, bits.len());
    (value, ptr)
}

const VERSION_SIZE: usize = 3;
const TYPE_SIZE: usize = 3;
const N_PACKET_INT_SIZE: usize = 11;
const TOTAL_LENGTH_INT_SIZE: usize = 15;

impl Packet {
    fn build(data: &[u8], mut ptr: usize) -> (Self, usize) {
        // let ptr = 0;
        let version;
        let type_id;
        (version, ptr) = parse_int(data, ptr, VERSION_SIZE);
        (type_id, ptr) = parse_int(data, ptr, TYPE_SIZE);
        let content = if type_id == 4 {
            let value;
            (value, ptr) = parse_literal(data, ptr);
            PacketContent::Literal(value)
        } else {
            let length_bit;
            (length_bit, ptr) = parse_int(data, ptr, 1);
            let length_type = if length_bit == 1 {
                let value;
                (value, ptr) = parse_int(data, ptr, N_PACKET_INT_SIZE);
                LengthType::NPackets(value.try_into().unwrap())
            } else {
                let value;
                (value, ptr) = parse_int(data, ptr, TOTAL_LENGTH_INT_SIZE);
                LengthType::TotalLength(value.try_into().unwrap())
            };
            let subpackets = match length_type {
                LengthType::NPackets(n) => {
                    let mut pkts = Vec::new();
                    for _ in 0..n {
                        let pkt;
                        (pkt, ptr) = Packet::build(data, ptr);
                        pkts.push(pkt);
                    }
                    pkts
                }
                LengthType::TotalLength(length) => {
                    let sub_data = &data[ptr..ptr + length];
                    ptr += length;
                    let mut sub_ptr: usize = 0;
                    let mut pkts = Vec::new();
                    while sub_ptr < length {
                        let pkt;
                        (pkt, sub_ptr) = Packet::build(sub_data, sub_ptr);
                        pkts.push(pkt);
                    }
                    pkts
                }
            };
            PacketContent::Operator {
                length_type,
                subpackets,
            }
        };
        (
            Self {
                version,
                type_id,
                content,
            },
            ptr,
        )
    }

    fn version_sum(&self) -> u64 {
        let sub_sum = match &self.content {
            PacketContent::Literal(_) => 0,
            PacketContent::Operator {
                length_type: _,
                subpackets,
            } => subpackets.iter().map(|p| p.version_sum()).sum(),
        };
        sub_sum + self.version
    }

    fn value(&self) -> u64 {
        match &self.content {
            PacketContent::Literal(val) => *val,
            PacketContent::Operator {
                length_type: _,
                subpackets,
            } => {
                let pkt_iter = subpackets.iter().map(|p| p.value());
                let check_is_two_long = || assert!(subpackets.len() == 2);
                let to_int = |x: bool| if x { 1_u64 } else { 0 };
                match self.type_id {
                    0 => pkt_iter.sum(),     //sum
                    1 => pkt_iter.product(), //product
                    2 => pkt_iter.min().unwrap(),
                    3 => pkt_iter.max().unwrap(),
                    5 => {
                        check_is_two_long();
                        to_int(subpackets[0].value() > subpackets[1].value())
                    }
                    6 => {
                        check_is_two_long();
                        to_int(subpackets[0].value() < subpackets[1].value())
                    }
                    7 => {
                        check_is_two_long();
                        to_int(subpackets[0].value() == subpackets[1].value())
                    }
                    n => panic!("Unexpected value of type_id: {}", n),
                }
            }
        }
    }
}

impl FromStr for Packet {
    type Err = StringParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (pkt, _) = Self::build(&expand_hex(s), 0);
        Ok(pkt)
    }
}

fn main() {
    let input = &utils::input_lines(16)[0];
    let pkt = Packet::from_str(input).unwrap();
    let part_1_answer = pkt.version_sum();
    println!("Day 16, Part 1 answer: {}", part_1_answer);
    let part_2_answer = pkt.value();
    println!("Day 16, Part 2 answer: {}", part_2_answer);
}

#[cfg(test)]
mod test;
