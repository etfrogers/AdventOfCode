import day6


def test_1():
    with open('day6_test_input.txt') as file:
        scrambled = file.readlines()
    plaintext = day6.unscramble(scrambled)
    assert plaintext == 'easter'


def test_part1():
    with open('day6_input.txt') as file:
        scrambled = file.readlines()
    plaintext = day6.unscramble(scrambled)
    assert plaintext == 'qrqlznrl'


def test_2():
    with open('day6_test_input.txt') as file:
        scrambled = file.readlines()
    plaintext = day6.unscramble(scrambled, modified=True)
    assert plaintext == 'advent'


def test_part2():
    with open('day6_input.txt') as file:
        scrambled = file.readlines()
    plaintext = day6.unscramble(scrambled, modified=True)
    assert plaintext == 'kgzdfaon'
