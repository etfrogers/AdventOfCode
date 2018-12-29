from AOC2018.day19 import day19, assembly
import nose

long_tests = False

test_program = '''#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5'''

# ip=0 [0, 0, 0, 0, 0, 0] seti 5 0 1
# ip=1 [1, 5, 0, 0, 0, 0] seti 6 0 2
# ip=2 [2, 5, 6, 0, 0, 0] addi 0 1 0
# ip=4 [4, 5, 6, 0, 0, 0] setr 1 0 0
# ip=6 [6, 5, 6, 0, 0, 0] seti 9 0 5

results_string = '''0, 5, 0, 0, 0, 0
1, 5, 6, 0, 0, 0
3, 5, 6, 0, 0, 0
5, 5, 6, 0, 0, 0
6, 5, 6, 0, 0, 9'''

results = [tuple(int(v) for v in line.split(', ')) for line in results_string.split('\n')]

# nose.run(argv=['', '-w../day16', '-v'])


def test1():
    device = day19.JumpDevice()
    device.run(test_program)
    assert device.registers[0] == 6


def line_runner(device, program, limit, expected):
    device.run(program, limit)
    assert tuple(device.registers) == tuple(expected)


def test_lines():
    device = day19.JumpDevice()
    prog = test_program.split('\n')
    for i, result in enumerate(results):
        yield line_runner, device, prog, i+1, result


part1_expected = (2016, 941, 940, 256, 941, 1)


def test_part1_assembly():
    result = assembly.run([0] + [0] * 5)
    assert result[0] == part1_expected[0]
    assert result[2] == part1_expected[2]


def test_part1_assembly_renamed():
    result = assembly.run_renamed(part2=False)
    assert result[0] == part1_expected[0]
    assert result[1] == part1_expected[2]


def test_part1_assembly_target():
    result = assembly.run_target(part2=False)
    assert result[0] == part1_expected[0]
    assert result[1] == part1_expected[2]


def test_part1_assembly_for_loops():
    result = assembly.run_for_loops(part2=False)
    assert result[0] == part1_expected[0]
    assert result[1] == part1_expected[2]


def test_part1_assembly_list_comps():
    result = assembly.run_list_comps(part2=False)
    assert result[0] == part1_expected[0]
    assert result[1] == part1_expected[2]


def test_part1_assembly_direct():
    result = assembly.run_direct(part2=False)
    assert result[0] == part1_expected[0]
    assert result[1] == part1_expected[2]


def test_target1():
    with open('input.txt') as f:
        program = f.read()
    device = day19.JumpDevice()
    device.run(program, limit=100)
    vm = device.registers[2]
    target = assembly.get_target(part2=False)
    assert vm == target


def test_target2a():
    with open('input.txt') as f:
        program = f.read()
    device = day19.JumpDevice()
    device.run(program, registers=[1] + [0] * 5, limit=100)
    vm = device.registers[2]
    target = assembly.run(registers=[1] + [0] * 5, do_loop=False)[2]
    assert vm == target


def test_target2b():
    with open('input.txt') as f:
        program = f.read()
    device = day19.JumpDevice()
    device.run(program, registers=[1] + [0] * 5, limit=100)
    vm = device.registers[2]
    target = assembly.get_target(part2=True)
    assert vm == target


if long_tests:
    def test_part1_vm():
        with open('input.txt') as f:
            program = f.read()
        device = day19.JumpDevice()
        device.run(program)
        assert tuple(device.registers) == part1_expected


def test_part2():
    assert assembly.run_direct(part2=True) == (22674960, 10551340)
