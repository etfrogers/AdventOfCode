from AOC2018.day22 import day22

TEST_DEPTH = 510
TEST_TARGET = (10, 10)


def test_map():
    cave = day22.Cave(depth=TEST_DEPTH, target=TEST_TARGET)
    assert cave.render((15, 15)) == map1


def test_risk():
    cave = day22.Cave(depth=TEST_DEPTH, target=TEST_TARGET)
    assert cave.risk_level() == 114


def check_indices(cave, coords, geologic_index, erosion_level, type_):
    assert cave.geologic_index[coords] == geologic_index
    assert cave.erosion_level[coords] == erosion_level
    assert cave.map[coords] == type_


def test_time():
    cave = day22.Cave(depth=TEST_DEPTH, target=TEST_TARGET)
    time = cave.time_to_target()
    assert time == 45


def test_coords():
    cave = day22.Cave(depth=TEST_DEPTH, target=TEST_TARGET)
    yield check_indices, cave, (0, 0), 0, 510, 0
    yield check_indices, cave, (1, 0), 16807, 17317, 1
    yield check_indices, cave, (0, 1), 48271, 8415, 0
    yield check_indices, cave, (1, 1), 145722555, 1805, 2
    yield check_indices, cave, (10, 10), 0, 510, 0


# At 0,0, the geologic index is 0. The erosion level is (0 + 510) % 20183 = 510. The type is 510 % 3 = 0, rocky.

# At 1,0, because the Y coordinate is 0, the geologic index is 1 * 16807 = 16807. The erosion level is (16807 + 510)
# % 20183 = 17317. The type is 17317 % 3 = 1, wet.

# At 0,1, because the X coordinate is 0, the geologic index is 1 * 48271 = 48271. The erosion level is (48271 + 510)
# % 20183 = 8415. The type is 8415 % 3 = 0, rocky.

# At 1,1, neither coordinate is 0 and it is not the coordinate of the target, so the geologic index is the erosion
# level of 0,1 (8415) times the erosion level of 1,0 (17317), 8415 * 17317 = 145722555. The erosion level is (
# 145722555 + 510) % 20183 = 1805. The type is 1805 % 3 = 2, narrow.

# At 10,10, because they are the target's coordinates, the geologic index is 0. The erosion level is (0 + 510) %
# 20183 = 510. The type is 510 % 3 = 0, rocky.

map1 = '''M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||'''