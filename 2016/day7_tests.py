import day7


def test1():
    addr = 'abba[mnop]qrst'  # supports TLS (abba outside square brackets).
    assert day7.supports_tls(addr)


def test2():
    addr = 'abcd[bddb]xyyx'
    # does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
    assert not day7.supports_tls(addr)


def test3():
    addr = 'aaaa[qwer]tyui'  # does not support TLS (aaaa is invalid; the interior characters must be different).
    assert not day7.supports_tls(addr)


def test4():
    addr = 'ioxxoj[asdfgh]zxcvbn'
    # supports TLS (oxxo is outside square brackets, even though it's within a larger string).
    assert day7.supports_tls(addr)


def test5():
    addr = 'ioxxoj[asdqyyqfgh]zxcvbn'
    assert not day7.supports_tls(addr)


def test6():
    addr = 'ioxxoj[asaaaagh]zxcvbn'
    assert day7.supports_tls(addr)


def test7():
    addr = 'ioxqoj[asaaaagh]zxcjkkjvbn'
    assert day7.supports_tls(addr)


def test8():
    addr = 'io11oj[asa11agh]zxcjkkjvbn'
    assert not day7.supports_tls(addr)


def test9():
    addr = 'io11oj[asa1aagh]zxcjkkjvbn'
    assert day7.supports_tls(addr)


def test10():
    addr = 'io11oj[asa1aagh]zxcjkkjv[sdaiouinnisa]bn'
    assert not day7.supports_tls(addr)


def test11():
    addr = 'io11oj[asa1aagh]zxcqjjqjkkjv[sdaiouinisabn]'
    assert day7.supports_tls(addr)


def test_ssl_1():
    addr = 'aba[bab]xyz'  # supports SSL (aba outside square brackets with corresponding bab within square brackets).
    assert day7.supports_ssl(addr)


def test_ssl_2():
    addr = 'xyx[xyx]xyx'  # does not support SSL (xyx, but no corresponding yxy).
    assert not day7.supports_ssl(addr)


def test_ssl_3():
    addr = 'aaa[kek]eke'  # supports SSL (eke in supernet with corresponding kek in hypernet;
    # the aaa sequence is not related, because the interior character must be different).
    assert day7.supports_ssl(addr)


def test_ssl_4():
    addr = 'zazbz[bzb]cdb'  # supports SSL (zaz has no corresponding aza,
    # but zbz has a corresponding bzb, even though zaz and zbz overlap).
    assert day7.supports_ssl(addr)


def test_part1():
    with open('day7_input.txt') as file:
        addrs = file.readlines()
    valid_ssl = [addr for addr in addrs if day7.supports_tls(addr)]
    assert len(valid_ssl) == 115


def test_part2():
    with open('day7_input.txt') as file:
        addrs = file.readlines()
    valid_ssl = [addr for addr in addrs if day7.supports_ssl(addr)]
    assert len(valid_ssl) == 231
