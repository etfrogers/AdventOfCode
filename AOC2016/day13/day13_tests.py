import day13


def test_1():
    office = day13.Office((7, 10), 10)
    print(str(office))
    assert str(office) == '''.#.####.##
..#..#...#
#....##...
###.#.###.
.##..#..#.
..##....#.
#...##.###'''


def test_is_odd1():
    assert day13.Office.is_odd(1)


def test_is_odd0():
    assert not day13.Office.is_odd(0)


def test_is_odd5():
    assert day13.Office.is_odd(5)


def test_is_odd101():
    assert day13.Office.is_odd(101)


def test_is_odd100():
    assert not day13.Office.is_odd(100)


def test_is_odd_m101():
    assert day13.Office.is_odd(-101)


def test_n_bits1():
    assert day13.Office.n_bits(1) == 1


def test_n_bits2():
    assert day13.Office.n_bits(2) == 1


def test_n_bits7():
    assert day13.Office.n_bits(7) == 3


def test_n_bits8():
    assert day13.Office.n_bits(8) == 1


def test_steps():
    office = day13.Office((7, 10), 10)
    assert office.steps_to((4, 7)) == 11


def test_part_1():
    office = day13.Office((50, 50), 1364)
    assert office.steps_to((39, 31)) == 86


def test_part_2():
    office = day13.Office((50, 50), 1364)
    assert office.reachable_locs(50) == 127
