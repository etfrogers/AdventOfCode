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

    def is_similar_to(self, other):
        assert len(self.label) == len(other.label)
        return len([1 for s, o in zip(self.label, other.label) if s == o]) == (len(self.label) - 1)

    def find_matched_letters(self, other):
        return ''.join([s for s, o in zip(self.label, other.label) if s == o])


def ids_with_letter_count(ids, count):
    return len([id for id in ids if id.has_letter_count(count)])


def get_checksum(ids):
    return ids_with_letter_count(ids, 2) * ids_with_letter_count(ids, 3)


def find_similar_ids(ids):
    for i, id in enumerate(ids):
        for other in ids[i:]:
            if id.is_similar_to(other):
                return id, other


if __name__ == '__main__':
    with open('input.txt') as f:
        input = f.readlines()
    ids = [BoxID(label.strip()) for label in input]
    cs = get_checksum(ids)
    print(cs)

    id1, id2 = find_similar_ids(ids)
    print(id1.find_matched_letters(id2))
