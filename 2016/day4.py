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
        checksum = sort_letters(letters)[:self.checksum_length]
        return ''.join(checksum)

    @property
    def decrypted_name(self):
        lst = [' ' if c == '-' else caesar(c, self.sector_id) for c in self.name]
        return ''.join(lst)


def sort_letters(letters):
    counter = Counter(letters)
    sorted_letters = []
    for count in sorted(list(set(counter.values())), reverse=True):
        this_count_inds = indexes(list(counter.values()), count)
        this_count_letters = [list(counter.keys())[i] for i in this_count_inds]
        sorted_letters += sorted(this_count_letters)
    return sorted_letters


def caesar(letter, n):
    return chr(ord('a') + ((ord(letter)-ord('a')+n) % 26))


def indexes(lst, value):
    return [i for i, v in enumerate(lst) if v == value]


def main():
    # names = '''aaaaa-bbb-z-y-x-123[abxyz]
    # a-b-c-d-e-f-g-h-987[abcde]
    # not-a-real-room-404[oarel]
    # totally-real-room-200[decoy]'''
    # names = names.split('\n')
    # names = ['rgllk-qss-etubbuzs-430[sblue]']

    with open('day4 input.txt') as file:
        names = file.readlines()
    rooms = [Room(name) for name in names]
    n_real = sum([1 for r in rooms if r.is_real])
    print(n_real)
    total = sum([r.sector_id for r in rooms if r.is_real])
    print(total)
    north_pole_room = [room for room in rooms if 'north' in room.decrypted_name]
    print(north_pole_room[0].decrypted_name, north_pole_room[0].sector_id)


if __name__ == '__main__':
    main()