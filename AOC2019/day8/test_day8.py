from AOC2019.day8.day8 import build_image, find_densest_layer, calc_checksum
import numpy as np


test_input = '123456789012'


def test_1():
    image = build_image(test_input, x=3, y=2)
    expected_0 = np.array([[1, 2, 3], [4, 5, 6]])
    expected_1 = np.array([[7, 8, 9], [0, 1, 2]])
    assert np.all(expected_0 == image[0, :, :])
    assert np.all(expected_1 == image[1, :, :])


def test_2():
    image = build_image(test_input, x=3, y=2)
    layer = find_densest_layer(image)
    assert layer == 0


def test_3():
    image = build_image(test_input, x=3, y=2)
    layer = find_densest_layer(image)
    checksum = calc_checksum(image, layer)
    assert checksum == 1


def test_part1():
    with open('input.txt') as f:
        pixels = f.read()
    image = build_image(pixels, x=25, y=6)
    layer = find_densest_layer(image)
    assert layer == 7
    checksum = calc_checksum(image, layer)
    assert checksum == 1677

