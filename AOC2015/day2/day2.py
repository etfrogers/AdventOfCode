import operator
from functools import reduce
from itertools import product


def parse_present(sizes):
    return tuple(int(v) for v in sizes.split('x'))


def paper_needed(size):
    sides = get_sides(size)
    return sum([2*s for s in sides]) + min(sides)


def get_sides(size):
    sides = (size[0] * size[1], size[0] * size[2], size[1] * size[2])
    return sides


def get_perimeters(size):
    perims = (2*(size[0]+size[1]), 2*(size[0]+size[2]), 2*(size[1]+size[2]))
    return perims


def ribbon_needed(size):
    perimeters = get_perimeters(size)
    return min(perimeters) + reduce(operator.mul, size)


def main():
    with open('input.txt') as f:
        present_list = f.readlines()
    sizes = [parse_present(p) for p in present_list]
    paper = [paper_needed(s) for s in sizes]
    print(f'Part 1: Total paper needed is {sum(paper)}')

    ribbon = [ribbon_needed(s) for s in sizes]
    print(f'Part 2: Total ribbon needed is {sum(ribbon)}')


if __name__ == '__main__':
    main()
