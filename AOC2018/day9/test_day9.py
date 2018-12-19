from AOC2018.day9 import day9


def test_1():
    n_players = 9
    last_marble = 25
    high_score = day9.play_marbles(n_players, last_marble)
    assert high_score == 32


def test_2():
    n_players = 10
    last_marble = 1618
    high_score = day9.play_marbles(n_players, last_marble)
    assert high_score == 8317


def test_3():
    n_players = 13
    last_marble = 7999
    high_score = day9.play_marbles(n_players, last_marble)
    assert high_score == 146373


def test_4():
    n_players = 17
    last_marble = 1104
    high_score = day9.play_marbles(n_players, last_marble)
    assert high_score == 2764


def test_5():
    n_players = 21
    last_marble = 6111
    high_score = day9.play_marbles(n_players, last_marble)
    assert high_score == 54718


def test_6():
    n_players = 30
    last_marble = 5807
    high_score = day9.play_marbles(n_players, last_marble)
    assert high_score == 37305


def test_7():
    n_players = 9
    last_marble = 48
    high_score = day9.play_marbles(n_players, last_marble)
    assert high_score == 63


def test_8():
    n_players = 1
    last_marble = 48
    high_score = day9.play_marbles(n_players, last_marble)
    assert high_score == 95


def test_9():
    n_players = 9
    last_marble = 92
    high_score = day9.play_marbles(n_players, last_marble)
    assert high_score == 107
