import day5


def test_whole_password():
    door_id = 'abc'
    pw = day5.get_password(door_id)
    assert pw == '18f47a30'


def test_part1():
    door_id = 'uqwqemis'
    pw = day5.get_password(door_id)
    assert pw == '1a3099aa'


def test_whole_password2():
    door_id = 'abc'
    pw = day5.get_password(door_id, part2=True)
    assert pw == '05ace8e3'


def test_part2():
    door_id = 'uqwqemis'
    pw = day5.get_password(door_id, part2=True)
    assert pw == '694190cd'
