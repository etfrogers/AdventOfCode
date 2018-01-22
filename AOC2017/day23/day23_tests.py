from AOC2017.day23 import day23


def test_part1():
    with open('input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    coproc = day23.CoProc(instructions)
    coproc.execute()
    assert coproc.mul_count == 6724


def test_rawcode_part1():
    mul, _ = day23.rawcode2()
    assert mul is None or mul == 6724


def test_multi_b_values():
    for b in range(80, 100, 2):
        yield rawcode_equals_complex_code, b
    # for b in range(100, 1000, 17):
    #     yield rawcode_equals_complex_code, b


def rawcode_equals_complex_code(b):
    _, registers_raw = day23.rawcode2(b_in=b)
    with open('input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    instructions[0] = 'set b ' + str(b)
    coproc = day23.CoProc(instructions)
    coproc.execute()
    reg_list = sorted(coproc.registers.items())
    registers_complex = (v for k, v in reg_list)
    assert all([c == r for c, r in zip(registers_complex, registers_raw)])
