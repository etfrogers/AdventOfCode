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

    for b in range(80, 100, 7):
        for end in range(b, b+(17*3), 17):
            yield rawcode_equals_complex_code, b, end


def rawcode_equals_complex_code(b, c=None):
    _, registers_raw = day23.rawcode2(b_in=b, end_in=c)
    with open('input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    instructions[0] = 'set b ' + str(b)
    if c is not None:
        instructions[1] = 'set c ' + str(c)
    coproc = day23.CoProc(instructions)
    coproc.execute()
    reg_list = sorted(coproc.registers.items())
    registers_complex = (v for k, v in reg_list)
    registers_complex = tuple(registers_complex)
    print(registers_raw)
    print(registers_complex)
    assert all([c == r for c, r in zip(registers_complex, registers_raw)])
