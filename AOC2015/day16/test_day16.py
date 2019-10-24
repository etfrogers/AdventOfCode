from AOC2015.day16.day16 import AuntSue


def test_part_1():
    test_spec = 'Sue 0: children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, vizslas: 0, ' \
                'goldfish: 5, trees: 3, cars: 2, perfumes: 1'
    with open('input.txt') as f:
        specs = f.readlines()
    sues = [AuntSue(s) for s in specs]
    test_sue = AuntSue(test_spec)

    matching_sue = [sue for sue in sues if sue == test_sue][0]
    assert matching_sue.number == 103


def test_part_2():
    test_spec = 'Sue 0: children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, vizslas: 0, ' \
                'goldfish: 5, trees: 3, cars: 2, perfumes: 1'
    with open('input.txt') as f:
        specs = f.readlines()
    sues = [AuntSue(s) for s in specs]
    test_sue = AuntSue(test_spec)

    matching_sue = [sue for sue in sues if test_sue.matches(sue)][0]
    assert matching_sue.number == 405
