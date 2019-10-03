from AOC2016.day15.day15 import Discs

TEST_INPUT = '''Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.'''


def test_parsing():
    discs = Discs()
    discs.parse_specs(TEST_INPUT.split('\n'))

    assert discs[1].n_positions == 5
    assert discs[1].start_pos == 4
    assert discs[2].n_positions == 2
    assert discs[2].start_pos == 1


def test_start_time():
    discs = Discs()
    discs.parse_specs(TEST_INPUT.split('\n'))

    start_time = discs.find_path_start_time()
    assert start_time == 5
