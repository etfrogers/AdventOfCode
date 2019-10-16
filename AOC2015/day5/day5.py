import re
from functools import reduce

VOWEL_PATTERN = re.compile(r'[aeiou]')
DOUBLE_LETTER_PATTERN = re.compile(r'([a-z])\1')
FORBIDDEN_STRINGS = ['ab', 'cd', 'pq', 'xy']


def has_three_vowels(string):
    matches = VOWEL_PATTERN.findall(string)
    return len(matches) >= 3


def has_double_letter(string):
    match = DOUBLE_LETTER_PATTERN.search(string)
    return match is not None


def has_forbidden_strings(string):
    return any([s in string for s in FORBIDDEN_STRINGS])


def is_nice(string: str):
    return has_three_vowels(string) and has_double_letter(string) and not has_forbidden_strings(string)


def main():
    with open('input.txt') as f:
        strings = f.readlines()
    nice_strings = [is_nice(string) for string in strings]

    print(f'Part 1: number of nice strings is {nice_strings.count(True)}')


if __name__ == '__main__':
    main()