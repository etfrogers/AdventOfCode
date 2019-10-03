from AOC2016.day18.day18 import Room


def test_1():
    first_row = '..^^.'
    n_rows = 3
    output = '''..^^.
.^^^^
^^..^'''

    room = Room(first_row, n_rows)
    assert room.render() == output


def test_2():
    first_row = '.^^.^.^^^^'
    n_rows = 10
    output = '''.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^'''

    room = Room(first_row, n_rows)
    assert room.render() == output
    assert room.n_safe_squares == 38