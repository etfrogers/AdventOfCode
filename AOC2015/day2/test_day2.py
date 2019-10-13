from AOC2015.day2.day2 import parse_present, paper_needed, ribbon_needed


def test_1():
    sizes = '2x3x4'
    size = parse_present(sizes)
    assert size == (2, 3, 4)
    paper = paper_needed(size)
    assert paper == 58


def test_2():
    sizes = '1x1x10'
    size = parse_present(sizes)
    assert size == (1, 1, 10)
    paper = paper_needed(size)
    assert paper == 43


def test_ribbon():
    sizes = '2x3x4'
    size = parse_present(sizes)
    ribbon = ribbon_needed(size)
    assert ribbon == 34


def test_ribbon2():
    sizes = '1x1x10'
    size = parse_present(sizes)
    ribbon = ribbon_needed(size)
    assert ribbon == 14
