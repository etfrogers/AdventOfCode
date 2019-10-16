from AOC2015.day10.day10 import look_and_say

test_cases = [('1', '11'),  # (1 copy of digit 1).
              ('11', '21'),  # (2 copies  of digit 1).
              ('21', '1211'),  # (one 2 followed by one 1).
              ('1211', '111221'),  # (one 1, one 2, and two 1s).
              ('111221', '312211'),  # (three 1s, two 2s, and one 1)
              ]


def check_look_and_say(case):
    output = look_and_say(case[0])
    assert output == case[1]


def test_1():
    for case in test_cases:
        yield check_look_and_say, case
