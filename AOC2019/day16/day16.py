import numpy as np
from functools import lru_cache
BASE_PATTERN = np.array([0, 1, 0, -1])


@lru_cache(maxsize=None)
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


def fft_phase2(lst: np.ndarray, offset: int) -> np.ndarray:
    assert offset > lst.size / 2

    output = np.zeros_like(lst)
    vals = np.abs(np.cumsum(lst[:offset-1:-1])) % 10
    output[:offset-1:-1] = vals
    return output


def fft(input_, n_phases, offset=None):
    lst = np.array([int(v) for v in input_], dtype=int)
    for _ in range(n_phases):
        if offset:
            lst = fft_phase2(lst, offset)
        else:
            lst = fft_phase(lst)
    output = ''.join([str(v) for v in lst])
    return output


def get_fft_message(input_, n_phases):
    repeats = 10_000
    offset = int(input_[:7])
    output = fft(input_*repeats, n_phases, offset)
    msg = output[offset:offset+8]
    return msg


def main():
    with open('input.txt') as file:
        input_ = file.read().strip()
    output = fft(input_, 100)
    print(output)
    print(f'First 8 chars: {output[:8]}')

    msg = get_fft_message(input_, 100)
    print(f'FFT message is: {msg}')


if __name__ == '__main__':
    main()
