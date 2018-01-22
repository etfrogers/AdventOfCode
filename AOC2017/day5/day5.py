
def in_bounds(inst, pos):
    return 0 <= pos < len(inst)


def to_str(inst, pos):
    out_list = [str(i) for i in inst]
    out_list[pos] = '(' + out_list[pos] + ')'
    return ' '.join(out_list)


def count_jumps(inst, part2=False):
    pos = 0
    steps = 0
    while in_bounds(inst, pos):
        # print(to_str(inst, pos))
        curr_inst = inst[pos]
        if part2:
            inst[pos] += -1 if (inst[pos] >= 3) else 1
        else:
            inst[pos] += 1
        pos = pos+curr_inst
        steps += 1
    return steps


def main():
    with open('input.txt', 'r') as file:
        inst = file.readlines()
    inst = [line.strip() for line in inst]
    inst = [int(l) for l in inst]
    # inst = [0, 3, 0, 1, -3]
    print(inst)
    count = count_jumps(inst, True)
    print(count)


if __name__ == '__main__':
    main()
