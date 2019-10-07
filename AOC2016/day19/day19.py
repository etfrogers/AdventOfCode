import time
from collections import deque, namedtuple
from datetime import datetime


class Elf:
    def __init__(self, id_, presents, prev=None, next_=None):
        self.id = id_
        self.presents = presents
        self.prev = prev
        self.next = next_
        self.deleted = False

    def delete(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.deleted = True

    def __repr__(self):
        if not self.deleted:
            return f'{self.id}:{self.presents}, next->{self.next.id}, prev->{self.prev.id}'
        else:
            return f"{self.id}:[deleted]"


def run_white_elephant(n, part2=False):
    elves = [Elf(i+1, 1) for i in range(n)]
    for i, elf in enumerate(elves):
        elf.prev = elves[(i-1) % n]
        elf.next = elves[(i+1) % n]
    start_elf = elves[0]
    if part2:
        next_elf = elves[len(elves) // 2]
    else:
        next_elf = elves[1]
    for i in range(n-1):
        start_elf.presents += next_elf.presents
        next_elf.delete()
        start_elf = start_elf.next
        if part2:
            next_elf = next_elf.next
            if (n-i) % 2 == 1:
                next_elf = next_elf.next
        else:
            next_elf = start_elf.next

    assert start_elf.presents == n
    return start_elf.id


def main():
    n_elves = 3004953
    print('Part 1: Remaining elf is ', run_white_elephant(n_elves))

    print('Part 2: Remaining elf is ', run_white_elephant(n_elves, part2=True))


if __name__ == '__main__':
    main()
