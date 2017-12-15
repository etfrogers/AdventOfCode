import numpy as np


def do_knot_hash(n, lengths):
    array = np.array(range(0, n))

    skip_size = 0
    position = 0

    for length in lengths:
        if length != 0:
            indexes = (np.array(list(range(0, length))) + position) % n
            array[indexes] = np.flipud(array[indexes])
        position = (position + length + skip_size) % n
        skip_size += 1
    return array


def calc_output(results):
    return results[0] * results[1]


def main():
    lengths = np.loadtxt('input.txt', dtype=int)
    n = 256
    # lengths = [3, 4, 1, 5]
    # n = 5
    results = do_knot_hash(n, lengths)
    print(results)
    output = calc_output(results)
    print(output)


if __name__ == '__main__':
    main()
