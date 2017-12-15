import day11


def test_hex_dist1():
    inst = 'ne,ne,ne'.split(',')
    dist = day11.hex_dist(day11.hex_walk(inst))
    assert dist == 3


def test_hex_dist2():
    inst = 'ne,ne,sw,sw'.split(',')
    dist = day11.hex_dist(day11.hex_walk(inst))
    assert dist == 0


def test_hex_dist3():
    inst = 'ne,ne,s,s'.split(',')
    dist = day11.hex_dist(day11.hex_walk(inst))
    assert dist == 2


def test_hex_dist4():
    inst = 'se,sw,se,sw,sw'.split(',')
    dist = day11.hex_dist(day11.hex_walk(inst))
    assert dist == 3


def test_part1():
    with open('input.txt', 'r') as file:
        path = file.read()
    path = path.strip()
    path = path.split(',')
    pos = day11.hex_walk(path)
    assert day11.hex_dist(pos) == 720
