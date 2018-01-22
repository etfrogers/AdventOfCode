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


def test_basic_track_0_1():
    n = 9
    step = 3
    _, buffer = day17.calc_spinlock(n, step)
    basic_after_0 = buffer[buffer.index(0)+1]
    assert basic_after_0 == 9


def test_track_0_1():
    n = 9
    step = 3
    assert day17.spinlock_track_0(n, step) == 9


def test_track_0_2017():
    n = 2017
    step = 3
    _, buffer = day17.calc_spinlock(n, step)
    basic_after_0 = buffer[buffer.index(0)+1]
    print(basic_after_0)
    assert basic_after_0 == day17.spinlock_track_0(n, step)


def test_part():
    n = 50000000
    step = 349
    assert day17.spinlock_track_0(n, step) == 47949463
