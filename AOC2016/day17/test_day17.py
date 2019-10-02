from AOC2016.day17.day17 import hash_chars, find_open_doors, find_shortest_path, stays_inside_walls, \
    find_longest_path_length


def test_hash1():
    code = 'hijkl'
    hash_ = hash_chars(code)
    expected = 'ced9'
    assert hash_ == expected


def test_hash2():
    code = 'hijklD'
    hash_ = hash_chars(code)
    expected = 'f2bc'
    assert hash_ == expected


def test_open_doors1():
    code = 'hijkl'
    doors = find_open_doors(code)
    expected = 'UDL'
    assert doors == expected


def test_open_doors2():
    code = 'hijklD'
    doors = find_open_doors(code)
    expected = 'ULR'
    assert doors == expected


def test_open_doors3():
    code = 'hijklDR'
    doors = find_open_doors(code)
    expected = ''
    assert doors == expected


def test_open_doors4():
    code = 'hijklDU'
    doors = find_open_doors(code)
    expected = 'R'
    assert doors == expected


def test_open_doors5():
    code = 'hijklDUR'
    doors = find_open_doors(code)
    expected = ''
    assert doors == expected


def test_path1():
    passcode = 'ihgpwlah'
    path = find_shortest_path(passcode)
    expected = 'DDRRRD'
    assert path == expected


def test_path2():
    passcode = 'kglvqrro'
    path = find_shortest_path(passcode)
    expected = 'DDUDRLRRUDRD'
    assert path == expected


def test_path3():
    passcode = 'ulqzkmiv'
    path = find_shortest_path(passcode)
    expected = 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'
    assert path == expected


def test_walls1():
    route = 'L'
    expected = False
    assert stays_inside_walls(route) == expected


def test_walls2():
    route = 'DDUUDUDUL'
    expected = False
    assert stays_inside_walls(route) == expected


def test_walls3():
    route = 'DDUUDUDURL'
    expected = True
    assert stays_inside_walls(route) == expected


def test_walls4():
    route = 'DDUUDUDURLRRR'
    expected = True
    assert stays_inside_walls(route) == expected


def test_walls5():
    route = 'DDUUDUDURLRRRR'
    expected = False
    assert stays_inside_walls(route) == expected


def test_walls6():
    route = 'DDDD'
    expected = False
    assert stays_inside_walls(route) == expected


def test_walls7():
    route = 'DDUDD'
    expected = True
    assert stays_inside_walls(route) == expected


def test_longest_path_length1():
    passcode = 'ihgpwlah'
    expected = 370
    assert find_longest_path_length(passcode) == expected


def test_longest_path_length2():
    passcode = 'kglvqrro'
    expected = 492
    assert find_longest_path_length(passcode) == expected


def test_longest_path_length3():
    passcode = 'ulqzkmiv'
    expected = 830
    assert find_longest_path_length(passcode) == expected
