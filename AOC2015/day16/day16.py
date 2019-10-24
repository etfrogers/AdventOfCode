import re
from collections import UserDict, defaultdict


class AuntSue(UserDict):
    SUE_PATTERN = re.compile(r'^Sue (\d+): ')
    COMPOUND_PATTERN = re.compile(r'(\w+\b(?<!^Sue)): (\d+)(, )?')
    TESTS = defaultdict(lambda: int.__eq__, [('cats', int.__gt__),
                                             ('trees', int.__gt__),
                                             ('pomeranians', int.__lt__),
                                             ('goldfish', int.__lt__),
                                             ])

    def __init__(self, spec):
        super().__init__()
        sue_match = self.SUE_PATTERN.search(spec)
        self.number = int(sue_match.group(1))
        for compound in self.COMPOUND_PATTERN.finditer(spec):
            self[compound.group(1)] = int(compound.group(2))

    def __eq__(self, other):
        for key, value in self.items():
            try:
                if other[key] != value:
                    return False
            except KeyError:
                # if the key is missing, assume equal
                pass
        return True

    def matches(self, other):
        for key, value in self.items():
            try:
                if not self.TESTS[key](other[key], value):
                    return False
            except KeyError:
                # if the key is missing, assume equal
                pass
        return True


def main():
    test_spec = 'Sue 0: children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, vizslas: 0, ' \
                'goldfish: 5, trees: 3, cars: 2, perfumes: 1'
    with open('input.txt') as f:
        specs = f.readlines()
    sues = [AuntSue(s) for s in specs]
    test_sue = AuntSue(test_spec)

    matching_sues = [sue for sue in sues if sue == test_sue]
    assert len(matching_sues) == 1
    matching_sue = matching_sues[0]
    print(f'Part 1: Matching sue is number {matching_sue.number} with a properties of {matching_sue}')

    matching_sues = [sue for sue in sues if test_sue.matches(sue)]
    assert len(matching_sues) == 1
    matching_sue = matching_sues[0]
    print(f'Part 2: Matching sue is number {matching_sue.number} with a properties of {matching_sue}')


if __name__ == '__main__':
    main()
