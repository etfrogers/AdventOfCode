import pytest
import numpy as np

from AOC2019.day16.day16 import fft, build_pattern, get_fft_message

test_inputs1 = ['12345678', '48226158', '34040438', '03415518', '01029498']
test_inputs2 = [('80871224585914546619083218645595', '24176176'),
                ('19617804207202209144916044189917', '73745418'),
                ('69317163492948606335995924319873', '52432133'),
                ]

test_patterns = [(3, np.array([0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1])),
                 (2, np.array([0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, -1, -1])),
                 ]


@pytest.mark.parametrize('n, expected', enumerate(test_inputs1))
def test_1(n, expected):
    input_ = test_inputs1[0]
    assert fft(input_, n) == expected


@pytest.mark.parametrize('input_, expected_8', test_inputs2)
def test_2(input_, expected_8):
    n = 100
    assert fft(input_, n)[:8] == expected_8


@pytest.mark.parametrize('i, expected', test_patterns)
def test_pattern(i, expected):
    pattern = build_pattern(i, len(expected))
    assert np.array_equal(pattern, expected)


def test_part1():
    with open('input.txt') as file:
        input_ = file.read().strip()
    output = fft(input_, 100)
    assert output[:8] == '89576828'


test_inputs3 = [('03036732577212944063491565474664', '84462026'),
                ('02935109699940807407585447034323', '78725270'),
                ('03081770884921959731165446850517', '53553731'),
                ]


@pytest.mark.parametrize('input_, expected_msg', test_inputs3)
def test_3(input_, expected_msg):
    n = 100
    assert get_fft_message(input_, n) == expected_msg


def test_part2():
    with open('input.txt') as file:
        input_ = file.read().strip()
    msg = get_fft_message(input_, 100)
    assert msg == '23752579'
