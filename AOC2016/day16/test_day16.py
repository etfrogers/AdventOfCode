from AOC2016.day16.day16 import expand, fill_disk, checksum, DISK_LENGTH, INPUT, DISK_LENGTH_2

expand_tests = [('1', '100'),
                ('0', '001'),
                ('11111', '11111000000'),
                ('111100001010', '1111000010100101011110000')]


def test_expand():
    for line in expand_tests:
        yield check_expand, line


def check_expand(pair):
    expanded = expand(pair[0])
    assert expanded == pair[1]


def test_fill_disk():
    input_ = '10000'
    disk_size = 20
    disk = fill_disk(input_, disk_size)
    assert disk == '10000011110010000111'


def test_checksum():
    cs = checksum('110010110100')
    assert cs == '100'


def test_disk_checksum():
    input_ = '10000'
    disk_size = 20
    disk = fill_disk(input_, disk_size)
    cs = checksum(disk)
    assert cs == '01100'


def test_part1():
    disk = fill_disk(INPUT, DISK_LENGTH)
    cs = checksum(disk)
    assert cs == '10011010010010010'


def test_part2():
    disk = fill_disk(INPUT, DISK_LENGTH_2)
    cs = checksum(disk)
    assert cs == '10101011110100011'
