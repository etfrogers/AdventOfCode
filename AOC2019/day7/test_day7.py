import pytest

from AOC2019.day7.day7 import optimise_phases

cases = [('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', 43210, (4, 3, 2, 1, 0)),
         ('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0', 54321, (0, 1, 2, 3, 4)),
         ('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0',
          65210, (1, 0, 4, 3, 2)),
         ]

cases2 = [('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5',
          139629729, (9, 8, 7, 6, 5)),
          (('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,' +
            '-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,' +
            '53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'), 18216, (9, 7, 8, 5, 6))
          ]


@pytest.mark.parametrize('instructions, expected_thrust, expected_phases', cases)
def test_1(instructions, expected_thrust, expected_phases):
    thrust, phases = optimise_phases(instructions)
    assert thrust == expected_thrust
    assert phases == expected_phases


def test_part1():
    with open('input.txt') as f:
        instructions = f.readline()
    thrust, phases = optimise_phases(instructions)
    assert thrust == 844468
    assert phases == (0, 2, 3, 4, 1)


@pytest.mark.parametrize('instructions, expected_thrust, expected_phases', cases2)
def test_2(instructions, expected_thrust, expected_phases):
    thrust, phases = optimise_phases(instructions, use_feedback=True)
    assert thrust == expected_thrust
    assert phases == expected_phases


def test_part2():
    with open('input.txt') as f:
        instructions = f.readline()
    thrust, phases = optimise_phases(instructions, use_feedback=True)
    assert thrust == 4215746
    assert phases == (6, 5, 8, 7, 9)
