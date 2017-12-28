import day17


def test_spinlock1():
    n = 2017
    step = 3
    value, _ = day17.calc_spinlock(n, step)
    assert value == 638


def test_spinlock2():
    n = 9
    step = 3
    _, buffer = day17.calc_spinlock(n, step)
    assert buffer == [0, 9, 5, 7, 2, 4, 3, 8, 6, 1]


def test_part1():
    n = 2017
    step = 349
    value, _ = day17.calc_spinlock(n, step)
    assert value == 640
