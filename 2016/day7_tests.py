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
