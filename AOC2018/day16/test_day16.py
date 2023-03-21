import itertools

from AOC2018.day16 import day16, reddit_day16


test_input = '''Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]'''

test_sample = day16.Sample(test_input.split('\n'))
device = day16.Device()

with open('day16/input.txt') as f:
    input_ = f.read()
input_ = input_.split('\n\n\n\n')

input_part1, input_part2 = ([line.strip() for line in part.split('\n')] for part in input_)
samples = day16.input_to_samples(input_part1)


def test1():
    assert device.n_opcodes(test_sample) == 3


def test_addr():
    input_state = (0, 1, 2, 3)
    command = (2, 3, 0)
    val = device.opcodes['addr'](input_state, command)
    test = (5, 1, 2, 3)
    assert all([v == t for v, t in zip(val, test)])


def test_setr():
    input_state = (0, 1, 2, 3)
    command = (2, 3, 0)
    val = device.opcodes['setr'](input_state, command)
    test = (2, 1, 2, 3)
    assert all([v == t for v, t in zip(val, test)])


def test_seti():
    input_state = (0, 1, 2, 3)
    command = (6, 3, 0)
    val = device.opcodes['seti'](input_state, command)
    test = (6, 1, 2, 3)
    assert all([v == t for v, t in zip(val, test)])


def test_eqir1():
    input_state = (0, 1, 2, 3)
    command = (3, 3, 0)
    val = device.opcodes['eqir'](input_state, command)
    test = (1, 1, 2, 3)
    assert all([v == t for v, t in zip(val, test)])


def test_eqir2():
    input_state = (0, 1, 2, 3)
    command = (1, 3, 0)
    val = device.opcodes['eqir'](input_state, command)
    test = (0, 1, 2, 3)
    assert all([v == t for v, t in zip(val, test)])


def test_labels():
    assert all([key == val.label for key, val in device.opcodes.items()])


def combi_reddit(reddit_func, input_, cmd, my_func, my_cmd):
    assert all([r == m for r, m in zip(reddit_func(input_, *cmd), my_func(input_, my_cmd))])


# def test_with_reddit():
#     for op in reddit_day16.OPERATIONS:
#         for input_ in itertools.product(range(0, 4, 2), repeat=4):
#             for cmd in itertools.product(range(4), repeat=3):
#                 my_cmd = (0,) + cmd
#                 yield combi_reddit, op, list(input_), list(cmd), device.opcodes[op.__name__], list(my_cmd)


def test_part1():

    n = sum([1 if device.n_opcodes(sample) >= 3 else 0 for sample in samples ])
    assert n == 493


def test_part2():

    device.build_opcode_mapping(samples)

    device.run(input_part2)

    assert device.registers[0] == 445