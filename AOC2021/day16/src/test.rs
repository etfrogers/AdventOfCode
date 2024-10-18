use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "D2FE28";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

fn bit_str_to_vec(str: &str) -> Vec<u8> {
    str.chars()
        .map(|b| String::from(b).parse().unwrap())
        .collect()
}

#[rstest]
#[case(TEST_1, "110100101111111000101000")]
#[case(
    "38006F45291200",
    "00111000000000000110111101000101001010010001001000000000"
)]
fn test_expand(#[case] input: &str, #[case] output: &str) {
    assert_eq!(expand_hex(input), bit_str_to_vec(output))
}

#[rstest]
fn test_build_simple() {
    let data = expand_hex("D2FE28");
    let (pkt, _ptr) = Packet::build(&data, 0);
    // assert_eq!(ptr, data.len() + 1);
    assert_eq!(pkt.version, 6);
    assert_eq!(pkt.type_id, 4);
    assert_eq!(pkt.content, PacketContent::Literal(2021));
}

#[rstest]
fn test_build_2() {
    let data = expand_hex("38006F45291200");
    let (pkt, _ptr) = Packet::build(&data, 0);
    assert_eq!(pkt.version, 1);
    assert_eq!(pkt.type_id, 6);
    assert!(matches!(pkt.content, PacketContent::Operator { .. }));
    if let PacketContent::Operator {
        length_type,
        subpackets,
    } = pkt.content
    {
        if let LengthType::TotalLength(n) = length_type {
            assert_eq!(n, 27)
        } else {
            panic!("failed to match LengthType")
        }
        assert_eq!(subpackets[0].content, PacketContent::Literal(10));
        assert_eq!(subpackets[1].content, PacketContent::Literal(20));
    } else {
        panic!("failed to match Operator")
    }
    // assert_eq!(pkt.content, PacketContent::Operator(_));
}

#[rstest]
fn test_build_3() {
    let data = expand_hex("EE00D40C823060");
    let (pkt, _ptr) = Packet::build(&data, 0);
    assert_eq!(pkt.version, 7);
    assert_eq!(pkt.type_id, 3);
    assert!(matches!(pkt.content, PacketContent::Operator { .. }));
    if let PacketContent::Operator {
        length_type,
        subpackets,
    } = pkt.content
    {
        if let LengthType::NPackets(n) = length_type {
            assert_eq!(n, 3)
        } else {
            panic!("failed to match LengthType")
        }
        assert_eq!(subpackets[0].content, PacketContent::Literal(1));
        assert_eq!(subpackets[1].content, PacketContent::Literal(2));
        assert_eq!(subpackets[2].content, PacketContent::Literal(3));
    } else {
        panic!("failed to match Operator")
    }
    // assert_eq!(pkt.content, PacketContent::Operator(_));
}

#[rstest]
#[case("8A004A801A8002F478", 16)]
#[case("620080001611562C8802118E34", 12)]
#[case("C0015000016115A2E0802F182340", 23)]
#[case("A0016C880162017C3686B18A3D4780", 31)]
fn test_version_sum(#[case] input: &str, #[case] sum: u64) {
    assert_eq!(Packet::from_str(input).unwrap().version_sum(), sum)
}

#[rstest]
#[case("C200B40A82", 3)]
#[case("04005AC33890", 54)]
#[case("880086C3E88112", 7)]
#[case("CE00C43D881120", 9)]
#[case("D8005AC2A8F0", 1)]
#[case("F600BC2D8F", 0)]
#[case("9C005AC2F8F0", 0)]
#[case("9C0141080250320F1802104A08", 1)]
fn test_value(#[case] input: &str, #[case] val: u64) {
    assert_eq!(Packet::from_str(input).unwrap().value(), val)
}

#[test]
fn test_part1() {
    let input = &utils::input_lines(16)[0];
    let pkt = Packet::from_str(input).unwrap();
    let part_1_answer = pkt.version_sum();

    assert_eq!(part_1_answer, 860);
}

#[test]
fn test_part2() {
    let input = &utils::input_lines(16)[0];
    let pkt = Packet::from_str(input).unwrap();
    let part_2_answer = pkt.value();

    assert_eq!(part_2_answer, 470949537659);
}
