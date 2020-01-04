import numpy as np

BASE_PATTERN = np.array([0, 1, 0, -1])


def build_pattern(i: int, length: int) -> np.ndarray:
    rep_pattern = np.tile(BASE_PATTERN, (i, 1)).flatten(order='f')
    n_reps = int(np.ceil(length / rep_pattern.size+1))
    pattern = np.tile(rep_pattern, (n_reps, ))
    return pattern[1:length+1]


def fft_phase(lst: np.ndarray) -> np.ndarray:
    output = np.zeros_like(lst)
    for i in range(len(lst)):
        pattern = build_pattern(i+1, lst.size)
        element = np.abs(np.sum(pattern * lst)) % 10
        output[i] = element
    return output


def fft(input_, n_phases):
    lst = np.array([int(v) for v in input_], dtype=int)
    for _ in range(n_phases):
        lst = fft_phase(lst)
    output = ''.join([str(v) for v in lst])
    return output


def main():
    with open('input.txt') as file:
        input_ = file.read().strip()
    output = fft(input_, 100)
    print(output)
    print(f'First 8 chars: {output[:8]}')


if __name__ == '__main__':
    main()
