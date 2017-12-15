
directions = {'n':  (+1, -1,  0),
              'nw': (+0, -1,  1),
              'sw': (-1,  0,  1),
              's':  (-1,  1,  0),
              'se': (+0,  1, -1),
              'ne': (+1,  0, -1)}


def hex_walk(instructions):
    pos = [0, 0, 0]
    all_dists = []
    for instruction in instructions:
        dir = directions[instruction]
        pos = [p+d for p, d in zip(pos, dir)]
        all_dists.append(hex_dist(pos))
    return pos


def hex_dist(pos):
    return max([abs(val) for val in pos])


def main():
    with open('input.txt', 'r') as file:
        path = file.read()
    path = path.strip()
    path = path.split(',')
    # path = ['ne', 'ne', 's', 's']
    pos = hex_walk(path)
    print(hex_dist(pos))


if __name__ == '__main__':
    main()