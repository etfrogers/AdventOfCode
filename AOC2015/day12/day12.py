import json
import re

DIGIT_PATTERN = re.compile(r'[-0-9]+')


def find_all_ints(string):
    matches = DIGIT_PATTERN.findall(string)
    return [int(v) for v in matches]


def sum_numbers(string, remove_red=False):
    if remove_red:
        data = json.loads(string)
        data = remove_red_items(data)
        string = json.dumps(data)
    return sum(find_all_ints(string))


def remove_red_items(data):
    if isinstance(data, list):
        return [remove_red_items(item) for item in data]
    elif isinstance(data, dict):
        if 'red' in data.keys() or 'red' in data.values():
            return None
        return {key: remove_red_items(value) for key, value in data.items()}
    else:
        return data


def main():
    with open('input.txt') as f:
        json_data = f.read()
    sum_ = sum_numbers(json_data)
    print(f'Part 1: Sum of all numbers  is {sum_}')

    sum_ = sum_numbers(json_data, remove_red=True)
    print(f'Part 2: Sum of all non-red numbers  is {sum_}')


if __name__ == '__main__':
    main()
