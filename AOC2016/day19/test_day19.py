from AOC2016.day19.day19 import run_white_elephant


def test_1():
    n = 5
    elf = run_white_elephant(n)
    assert elf == 3


def test_part_1():
    n = 3004953
    elf = run_white_elephant(n)
    assert elf == 1815603


def test_2():
    n = 5
    elf = run_white_elephant(n, part2=True)
    assert elf == 2
