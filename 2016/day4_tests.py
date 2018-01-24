import day4
from nose.tools import raises

def test_real1():
    # is a real room because the most common letters are a (5), b (3), and then a tie
    # between x, y, and z, which are listed alphabetically.
    data = 'aaaaa-bbb-z-y-x-123[abxyz]'
    assert day4.Room(data).is_real


def test_real2():
    # a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are all tied (1 of each),
    # the first five are listed alphabetically.
    data = 'a-b-c-d-e-f-g-h-987[abcde]'
    assert day4.Room(data).is_real


def test_real3():
    # not-a-real-room-404[oarel] is a real room.
    data = 'not-a-real-room-404[oarel]'
    assert day4.Room(data).is_real


def test_real4():
    data = 'totally-real-room-200[decoy]'
    assert not day4.Room(data).is_real


def test_real5():
    data = 'totalf-0[taflo]'
    assert day4.Room(data).is_real


@raises(ValueError)
def test_real6():
    data = 'totalf-[taflo]'
    assert day4.Room(data).is_real


def test_real6():
    data = 'rgllk-qss-etubbuzs-430[sblue]'
    assert day4.Room(data).is_real


def test_sum():
    names = '''aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]'''
    names = names.split('\n')
    rooms = [day4.Room(name) for name in names]
    total = sum([r.sector_id for r in rooms if r.is_real])
    assert total == 1514


def test_n_real():
    names = '''aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]'''
    names = names.split('\n')
    rooms = [day4.Room(name) for name in names]
    n_real = sum([1 for r in rooms if r.is_real])
    assert n_real == 3
