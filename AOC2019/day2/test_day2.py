import pytest

from AOC2019.day2.day2 import IntCodeComputer

cases = [('1,9,10,3,2,3,11,0,99,30,40,50', '3500,9,10,70,2,3,11,0,99,30,40,50'),
         ('1,0,0,0,99', '2,0,0,0,99'),
         ('2,3,0,3,99', '2,3,0,6,99'),
         ('2,4,4,5,99,0', '2,4,4,5,99,9801'),
         ('1,1,1,4,99,5,6,0,99', '30,1,1,4,2,5,6,0,99'),
         ]


@pytest.mark.parametrize('input_, output', cases)
def test_1(input_, output):
    comp = IntCodeComputer(input_)
    comp.execute()
    test_output = ','.join([str(v) for v in comp.instructions])
    assert test_output == output


def test_part1():
    with open('input.txt') as f:
        instructions = f.readline()

    comp = IntCodeComputer(instructions)
    comp.instructions[1] = 12
    comp.instructions[2] = 2
    comp.execute()
    assert comp.instructions[0] == 5482655
