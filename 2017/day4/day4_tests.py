import day4


def test_is_valid1():
    assert day4.is_valid('aa bb cc dd ee')


def test_is_valid2():
    assert not day4.is_valid('aa bb cc dd aa')


def test_is_valid3():
    assert day4.is_valid('aa bb cc dd aaa')


def test_part_1():
    with open('input.txt', 'r') as file:
        phrase_list = file.readlines()
    phrase_list = [line.strip() for line in phrase_list]
    count = day4.count_valid_phrases(phrase_list)
    assert count == 386


def test_is_valid_ana1():
    assert day4.is_valid('abcde fghij', True)


def test_is_valid_ana2():
    assert not day4.is_valid('abcde xyz ecdab', True)


def test_is_valid_ana3():
    assert day4.is_valid('a ab abc abd abf abj', True)


def test_is_valid_ana4():
    assert day4.is_valid('iiii oiii ooii oooi oooo', True)


def test_is_valid_ana5():
    assert not day4.is_valid('oiii ioii iioi iiio', True)


def test_part_2():
    with open('input.txt', 'r') as file:
        phrase_list = file.readlines()
    phrase_list = [line.strip() for line in phrase_list]
    count = day4.count_valid_phrases(phrase_list, True)
    assert count == 208
