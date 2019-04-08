from AOC2018.day13.day13 import CartTurnDir, Track, Direction


def test_dir_increment():
    expected_order = [CartTurnDir.LEFT, CartTurnDir.STRAIGHT, CartTurnDir.RIGHT, CartTurnDir.LEFT, CartTurnDir.STRAIGHT, CartTurnDir.RIGHT]
    direction = CartTurnDir(0)
    for expected_dir in expected_order:
        assert direction == expected_dir
        direction = direction.next()


simple_input = ['|',
                'v',
                '|',
                '|',
                '|',
                '^',
                '|']


def test_simple_parse():
    track = Track(simple_input)
    assert track.render_map() == ['|']*7
    assert len(track.carts) == 2
    assert track.carts[0].coords == (1, 0)
    assert track.carts[0].direction == Direction.SOUTH
    assert track.carts[1].coords == (5, 0)
    assert track.carts[1].direction == Direction.NORTH
