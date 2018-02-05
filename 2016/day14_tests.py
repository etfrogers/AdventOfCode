import day14


def test_contains_triple():
    salt = 'abc'
    candidate = day14.get_hash(salt, 18)
    triple, val = day14.contains_triple(candidate)
    assert triple
    assert val == '8'


def test_1():
    salt = 'abc'
    keys = day14.generate_keys(salt, 1)
    assert keys[0][0] == 39


def test_2():
    salt = 'abc'
    keys = day14.generate_keys(salt, 2)
    assert keys[-1][0] == 92


def test_64():
    salt = 'abc'
    keys = day14.generate_keys(salt, 64)
    assert keys[-1][0] == 22728


def test_part1():
    salt = 'zpqevtbw'
    keys = day14.generate_keys(salt, 64)
    assert keys[-1][0] == 16106