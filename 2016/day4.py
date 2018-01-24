import re
from collections import Counter


class Room:
    name_expr = re.compile('([-a-z]*)([0-9]*)\[([a-z]*)\]')
    checksum_length = 5

    def __init__(self, data):
        match = self.name_expr.match(data.strip())
        name_with_dash = match.group(1)
        assert name_with_dash[-1] == '-'
        self.name = name_with_dash[:-1]
        self.sector_id = int(match.group(2))
        self.checksum = match.group(3)
        assert len(self.checksum) == 5

    @property
    def is_real(self):
        return self.checksum_from_name() == self.checksum

    def checksum_from_name(self):

        letters = self.name.replace('-', '')
        counter = Counter(letters)
        common = counter.most_common(self.checksum_length)
        least_common_count = min([v for k, v in common])
        untied = [entry[0] for entry in common if entry[1] > least_common_count]

        tie_inds = indexes(list(counter.values()), least_common_count)
        ties = [list(counter.keys())[i] for i in tie_inds]
        n_ties_needed = self.checksum_length - len(untied)
        checksum = untied + sorted(ties)[:n_ties_needed]
        assert len(checksum) == 5
        return ''.join(checksum)


def indexes(lst, value):
    return [i for i, v in enumerate(lst) if v == value]


def main():
    names = '''aaaaa-bbb-z-y-x-123[abxyz]
    a-b-c-d-e-f-g-h-987[abcde]
    not-a-real-room-404[oarel]
    totally-real-room-200[decoy]'''
    names = names.split('\n')

    with open('day4 input.txt') as file:
        names = file.readlines()
    rooms = [Room(name) for name in names]
    total = sum([r.sector_id for r in rooms if r.is_real])
    print(total)


if __name__ == '__main__':
    main()