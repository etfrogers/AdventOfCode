import re

DIGIT_PATTERN = re.compile(r'[-0-9]+')


def find_all_ints(string):
    matches = DIGIT_PATTERN.findall(string)
    return [int(v) for v in matches]


def sum_numbers(string):
    return sum(find_all_ints(string))


def main():
    with open('input.txt') as f:
        json_data = f.read()
    sum_ = sum_numbers(json_data)
    print(f'Part 1: Sum of all numbers  is {sum_}')


if __name__ == '__main__':
    main()
