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
    *checks, diagnostic_code = comp.output_data
    assert diagnostic_code == 3122865
    assert all([v == 0 for v in checks])


@pytest.mark.parametrize('comparator', range(20))
def test_equal_8_pos(comparator):
    instructions = '3,9,8,9,10,9,4,9,99,-1,8'
    comp = IntCodeComputer2(instructions, [comparator])
    comp.execute()
    assert len(comp.output_data) == 1
    assert comp.output_data[0] == int(comparator == 8)


@pytest.mark.parametrize('comparator', range(20))
def test_less_8_pos(comparator):
    instructions = '3,9,7,9,10,9,4,9,99,-1,8'
    comp = IntCodeComputer2(instructions, [comparator])
    comp.execute()
    assert len(comp.output_data) == 1
    assert comp.output_data[0] == int(comparator < 8)


@pytest.mark.parametrize('comparator', range(20))
def test_equal_8_im(comparator):
    instructions = '3,3,1108,-1,8,3,4,3,99'
    comp = IntCodeComputer2(instructions, [comparator])
    comp.execute()
    assert len(comp.output_data) == 1
    assert comp.output_data[0] == int(comparator == 8)


@pytest.mark.parametrize('comparator', range(20))
def test_less_8_im(comparator):
    instructions = '3,3,1107,-1,8,3,4,3,99'
    comp = IntCodeComputer2(instructions, [comparator])
    comp.execute()
    assert len(comp.output_data) == 1
    assert comp.output_data[0] == int(comparator < 8)


@pytest.mark.parametrize('comparator', range(-5, 5))
def test_equal_zero_pos(comparator):
    instructions = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
    comp = IntCodeComputer2(instructions, [comparator])
    comp.execute()
    assert len(comp.output_data) == 1
    assert comp.output_data[0] == int(comparator != 0)


@pytest.mark.parametrize('comparator', range(-5, 5))
def test_equal_zero_im(comparator):
    instructions = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'
    comp = IntCodeComputer2(instructions, [comparator])
    comp.execute()
    assert len(comp.output_data) == 1
    assert comp.output_data[0] == int(comparator != 0)


@pytest.mark.parametrize('comparator', range(20))
def test_equal_8_complex(comparator):
    instructions = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,' + \
                   '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,' + \
                   '999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
    comp = IntCodeComputer2(instructions, [comparator])
    comp.execute()
    assert len(comp.output_data) == 1
    if comparator < 8:
        expected = 999
    elif comparator == 8:
        expected = 1000
    else:
        expected = 1001
    assert comp.output_data[0] == expected


def test_part2():
    with open('input.txt') as f:
        instructions = f.readline()

    comp = IntCodeComputer2(instructions, [5])
    comp.execute()
    assert comp.output_data.pop() == 773660
