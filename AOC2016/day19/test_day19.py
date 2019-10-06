from AOC2016.day19.day19 import run_white_elephant


def test_1():
    n = 5
    elf = run_white_elephant(n)
    assert elf == 3
