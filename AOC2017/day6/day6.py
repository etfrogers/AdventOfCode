
def do_balancing_cycle(blocks):
    max_value = max(blocks) 
    # Tuple.index returns first occurrence, which is required behaviour
    pos = blocks.index(max_value)
    blocks[pos] = 0
    for _ in range(max_value):
        # spread out over other blocks
        pos = (pos + 1) % len(blocks)
        blocks[pos] += 1


def balance_blocks(blocks):
    config_list = []
    cycles = 0
    while tuple(blocks) not in config_list[0:-1]:
        config_list.append(tuple(blocks))
        do_balancing_cycle(blocks)
        cycles += 1
    loop_length = len(config_list) - config_list.index(tuple(blocks))
    return cycles, loop_length, config_list


def main():
    # with open('puzzle_input.txt', 'r') as file:
    #     blocks = file.readlines()
    # blocks = [line.strip() for line in blocks]
    # blocks = [int(l) for l in blocks]
    puzzle_input = [4, 1, 15, 12, 0, 9, 9, 5, 5, 8, 7, 3, 14, 5, 12, 3]
    blocks = [0, 2, 7, 0]
    blocks = puzzle_input
    print(blocks)
    count, loop_length, config_list = balance_blocks(blocks)
    print(count)
    print(loop_length)


if __name__ == '__main__':
    main()