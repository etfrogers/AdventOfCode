import pytest

from AOC2019.day5.day5 import IntCodeComputer2

cases = [('1101,100,-1,4,0', '1101,100,-1,4,99'),
         ('1002,4,3,4,33', '1002,4,3,4,99')]


@pytest.mark.parametrize('input_, output', cases)
def test_1(input_, output):
    comp = IntCodeComputer2(input_)
    comp.execute()
    test_output = ','.join([str(v) for v in comp.instructions])
    assert test_output == output


def test_part1():
    with open('input.txt') as f:
        instructions = f.readline()

    comp = IntCodeComputer2(instructions, [1])
    comp.execute()
    assert all([v == 0 for v in comp.output_data[1:]])
    assert comp.output_data[0] == 3122865

