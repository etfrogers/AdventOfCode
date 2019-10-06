
def run_white_elephant(n):
    elves = [1] * n
    while elves.count(0) < (len(elves) - 1):  # all but one element is zero
        for i in range(len(elves)):
            if elves[i] == 0:
                continue
            else:
                next_elf = (i + 1) % len(elves)
                while elves[next_elf] == 0:
                    next_elf += 1
                    if next_elf == len(elves):
                        next_elf = 0
                elves[i] += elves[next_elf]
                elves[next_elf] = 0
    remaining_elf = elves.index(n)
    assert elves[remaining_elf] == n
    return remaining_elf + 1


def main():
    n_elves = 3004953
    print('Part 1: Remaining elf is ', run_white_elephant(n_elves))


if __name__ == '__main__':
    main()
