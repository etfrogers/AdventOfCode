from AOC2016.day20.day20 import IPList


def test_1():
    test_input = """5-8
0-2
4-7"""
    ip_list = IPList(9, test_input.split('\n'))
    # assert IPList.valid_ips == [3, 9]
    assert ip_list.min_valid_ip() == 3


def test_2():
    test_input = """3-3
0-2
4-7"""
    ip_list = IPList(9, test_input.split('\n'))
    # assert IPList.valid_ips == [8, 9]
    assert ip_list.min_valid_ip() == 8


def test_3():
    test_input = """3-3
1-2
4-7"""
    ip_list = IPList(9, test_input.split('\n'))
    # assert IPList.valid_ips == [0, 8, 9]
    assert ip_list.min_valid_ip() == 0


def test_4():
    test_input = """2-3
0-5
8-9"""
    ip_list = IPList(9, test_input.split('\n'))
    # assert IPList.valid_ips == [0, 8, 9]
    assert ip_list.min_valid_ip() == 6


def test_5():
    test_input = """2-4
0-5
8-9"""
    ip_list = IPList(9, test_input.split('\n'))
    # assert IPList.valid_ips == [0, 8, 9]
    assert ip_list.min_valid_ip() == 6


def test_6():
    test_input = """0-3
0-5
8-9"""
    ip_list = IPList(9, test_input.split('\n'))
    # assert IPList.valid_ips == [0, 8, 9]
    assert ip_list.min_valid_ip() == 6


def test_6():
    test_input = """0-5
0-5
8-9"""
    ip_list = IPList(9, test_input.split('\n'))
    # assert IPList.valid_ips == [0, 8, 9]
    assert ip_list.min_valid_ip() == 6
