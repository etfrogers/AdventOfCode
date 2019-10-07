import time
from collections import deque, namedtuple
from datetime import datetime

Elf = namedtuple('Elf', ['id', 'presents'])


def run_white_elephant(n, part2=False):
    elves = deque([Elf(i+1, 1) for i in range(n)])
    time1 = datetime.now()
    while len(elves) > 1:
        if len(elves) % 10000 == 0:
            # print(len(elves))
            time2 = datetime.now()
            elapsed = time2 - time1
            print(f'Time elapsed between {len(elves)} and {len(elves)+10000} is {elapsed.total_seconds()}')
            time1 = datetime.now()
        if part2:
            next_pos = len(elves) // 2
        else:
            next_pos = 1
        elves.rotate(-next_pos)
        next_elf = elves.popleft()
        elves.rotate(next_pos)
        id_ = elves[0].id
        presents = elves[0].presents + next_elf.presents
        elves[0] = Elf(id_, presents)
        elves.rotate(-1)

    remaining_elf = elves[0][0]
    assert elves[0][1] == n
    return remaining_elf


def main():
    n_elves = 3004953
    print('Part 1: Remaining elf is ', run_white_elephant(n_elves))

    print('Part 2: Remaining elf is ', run_white_elephant(n_elves, part2=True))


if __name__ == '__main__':
    main()
