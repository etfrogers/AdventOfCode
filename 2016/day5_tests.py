import day5


def test_whole_password():
    door_id = 'abc'
    pw = day5.get_password(door_id)
    assert pw == '18f47a30'


def test_part1():
    door_id = 'uqwqemis'
    pw = day5.get_password(door_id)
    assert pw == '1a3099aa'