from AOC2015.day4.day4 import get_lowest_decimal


def test_1():
    key = 'abcdef'
    decimal = get_lowest_decimal(key)
    assert decimal == 609043


def test_2():
    key = 'pqrstuv'
    decimal = get_lowest_decimal(key)
    assert decimal == 1048970


