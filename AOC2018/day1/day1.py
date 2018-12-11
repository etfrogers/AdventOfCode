from typing import Union, List


def parse_frequency_changes(starting_value: int, changes: Union[str, List[str]]):
    if isinstance(changes, str):
        changes = changes.split(', ')
    changes = [int(v) for v in changes]
    value = starting_value
    for change in changes:
        value += change
    return value


if __name__ == '__main__':
    with open('input.txt') as f:
        input = f.readlines()
    f = parse_frequency_changes(0, input)
    print(f)
