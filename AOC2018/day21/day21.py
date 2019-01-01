from AOC2018.day21.assembly import *


def main():
    part1 = assembly_refactor(0, 2)
    print('Part 1: ', part1[1])

    part2 = assembly_refactor(0)
    print('Part 2: ', part2[-1])


if __name__ == '__main__':
    main()
