import day9


def test_process_stream_n_groups1():
    stream = '{}'
    n_groups, _ = day9.process_stream(stream)
    assert n_groups == 1


def test_process_stream_n_groups2():
    stream = '{{{}}}'
    n_groups, _ = day9.process_stream(stream)
    assert n_groups == 3


def test_process_stream_n_groups3():
    stream = '{{},{}}'
    n_groups, _ = day9.process_stream(stream)
    assert n_groups == 3


def test_process_stream_n_groups4():
    stream = '{{{},{},{{}}}}'
    n_groups, _ = day9.process_stream(stream)
    assert n_groups == 6


def test_process_stream_n_groups5():
    stream = '{<{},{},{{}}>}'
    n_groups, _ = day9.process_stream(stream)
    assert n_groups == 1


def test_process_stream_n_groups6():
    stream = '{<a>,<a>,<a>,<a>}'
    n_groups, _ = day9.process_stream(stream)
    assert n_groups == 1


def test_process_stream_n_groups7():
    stream = '{{<a>},{<a>},{<a>},{<a>}}'
    n_groups, _ = day9.process_stream(stream)
    assert n_groups == 5


def test_process_stream_n_groups8():
    stream = '{{<!>},{<!>},{<!>},{<a>}}'
    n_groups, _ = day9.process_stream(stream)
    assert n_groups == 2


def test_process_stream_score1():
    stream = '{}'
    _, score = day9.process_stream(stream)
    assert score == 1


def test_process_stream_score2():
    stream = '{{{}}}'
    _, score = day9.process_stream(stream)
    assert score == 6


def test_process_stream_score3():
    stream = '{{},{}}'
    _, score = day9.process_stream(stream)
    assert score == 5


def test_process_stream_score4():
    stream = '{{{},{},{{}}}}'
    _, score = day9.process_stream(stream)
    assert score == 16


def test_process_stream_score5():
    stream = '{<a>,<a>,<a>,<a>}'
    _, score = day9.process_stream(stream)
    assert score == 1


def test_process_stream_score6():
    stream = '{{<ab>},{<ab>},{<ab>},{<ab>}}'
    _, score = day9.process_stream(stream)
    assert score == 9


def test_process_stream_score7():
    stream = '{{<!!>},{<!!>},{<!!>},{<!!>}}'
    _, score = day9.process_stream(stream)
    assert score == 9


def test_process_stream_score8():
    stream = '{{<a!>},{<a!>},{<a!>},{<ab>}}'
    _, score = day9.process_stream(stream)
    assert score == 3


def test_process_stream_part1():
    with open('input.txt', 'r') as file:
        stream = file.read()
    stream = stream.strip()
    n_groups, total_score = day9.process_stream(stream)
    assert n_groups == 1688
    assert total_score == 12897
