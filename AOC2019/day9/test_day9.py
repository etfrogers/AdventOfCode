import pytest

from AOC2019.day9.day9 import RelativeIntCodeComputer

cases = [('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99', [],
          [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]),
         ('1102,34915192,34915192,7,4,7,99,0', [], 'len_16'),
         ('104,1125899906842624,99', [], [1125899906842624]),
         ]


@pytest.mark.parametrize('instructions, input_, expected_output', cases)
def test_1(instructions, input_, expected_output):
    comp = RelativeIntCodeComputer(instructions, input_)
    comp.execute()
    if expected_output == 'len_16':
        assert len(str(comp.output_data[0])) == 16
    else:
        assert tuple(reversed(comp.output_data)) == tuple(expected_output)


def test_simple_relative_base():
    instructions = '109,2000,109,19,204,-34,99'
    instructions += ',' + ','.join([str(v) for v in range(7, 2000)])
    comp = RelativeIntCodeComputer(instructions, [])
    comp.execute()
    assert len(comp.output_data) == 1
    assert comp.output_data[0] == 1985


def test_part1():
    with open('input.txt') as f:
        instructions = f.readline()

    comp = RelativeIntCodeComputer(instructions, [1])
    comp.execute()
    assert len(comp.output_data) == 1
    assert comp.output_data[0] == 2671328082


def test_part2():
    with open('input.txt') as f:
        instructions = f.readline()
    comp = RelativeIntCodeComputer(instructions, [2])
    comp.execute()
    assert len(comp.output_data) == 1
    assert comp.output_data[0] == 59095
