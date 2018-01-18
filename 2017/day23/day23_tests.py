import day23


def test_part1():
    with open('input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    coproc = day23.CoProc(instructions)
    coproc.execute()
    assert coproc.mul_count == 6724