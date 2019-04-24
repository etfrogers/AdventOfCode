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


def test_stretching():
    salt = 'abc'
    candidate = day14.get_hash(salt, 0, stretch=True)
    assert candidate == 'a107ff634856bb300138cac6568c0f24'


def test_stretching_triple():
    salt = 'abc'
    candidate = day14.get_hash(salt, 5, stretch=True)
    triple, val = day14.contains_triple(candidate)
    assert triple
    assert val == '2'


def test_stretch_1():
    salt = 'abc'
    keys = day14.generate_keys(salt, 1, stretch=True)
    assert keys[0][0] == 10


def test_stretching_64():
    salt = 'abc'
    keys = day14.generate_keys(salt, 64, stretch=True)
    assert keys[-1][0] == 22551


def test_part2():
    salt = 'zpqevtbw'
    keys = day14.generate_keys(salt, 64, stretch=True)
    assert keys[-1][0] == 22423

