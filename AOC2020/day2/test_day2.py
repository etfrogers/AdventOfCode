from AOC2020.day2.day2 import is_valid, number_of_valid_passwords, is_valid2

test_input = ['1-3 a: abcde', '1-3 b: cdefg', '2-9 c: ccccccccc']


def test_is_valid():
    assert is_valid(test_input[0])
    assert not is_valid(test_input[1])
    assert is_valid(test_input[2])


def test_number():
    assert number_of_valid_passwords(test_input) == 2


def test_part_1():
    with open('input.txt') as file:
        password_list = file.readlines()
    password_list = [line.strip() for line in password_list]
    n = number_of_valid_passwords(password_list)
    assert n == 620


def test_is_valid2():
    assert is_valid2(test_input[0])
    assert not is_valid2(test_input[1])
    assert not is_valid2(test_input[2])


def test_number2():
    assert number_of_valid_passwords(test_input, part2=True) == 1
