

def reduce(polymer):
    prev_len = len(polymer)+1
    while len(polymer) < prev_len:
        prev_len = len(polymer)
        polymer = reduce_step(polymer)
    return polymer


def reduce_step(polymer):
    new_polymer = []
    i = 0
    while i < len(polymer)-1:
        if polymer[i] == polymer[i+1].swapcase():
            i += 1
        else:
            new_polymer.append(polymer[i])
        i += 1

    try:
        # last element is not appended in the loop, so do it here. Will raise exception if meant to skip it
        new_polymer.append(polymer[i])
    except IndexError:
        pass

    return ''.join(new_polymer)


if __name__ == '__main__':
    with open('input.txt') as f:
        input = f.read().strip()
    polymer = reduce(input)
    print(polymer)
    print(len(polymer))
