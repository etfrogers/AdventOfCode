from collections import Counter


class BoxID:
    def __init__(self, label):
        self.label = label
        self.counter = Counter(self.label)

    def is_two_letter(self):
        return self.has_letter_count(2)

    def is_three_letter(self):
        return self.has_letter_count(3)

    def has_letter_count(self, count: int):
        return any([v == count for v in self.counter.values()])


def ids_with_letter_count(ids, count):
    return len([id for id in ids if id.has_letter_count(count)])


def get_checksum(ids):
    return ids_with_letter_count(ids, 2) * ids_with_letter_count(ids, 3)


if __name__ == '__main__':
    with open('input.txt') as f:
        input = f.readlines()
    ids = [BoxID(label) for label in input]
    cs = get_checksum(ids)
    print(cs)
