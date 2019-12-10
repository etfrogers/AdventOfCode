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
