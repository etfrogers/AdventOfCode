from typing import Union, List


def normalise_changes(changes: Union[str, List[str]]):
    if isinstance(changes, str):
        changes = changes.split(', ')
    changes = [int(v) for v in changes]
    return changes


def parse_frequency_changes(starting_value: int, changes: Union[str, List[str]]):
    changes = normalise_changes(changes)
    value = starting_value
    for change in changes:
        value += change
    return value


def find_repeated_freq(starting_value: int, changes: Union[str, List[str]]):
    changes = normalise_changes(changes)
    value = starting_value
    prev_vals = []
    iterator = iter(changes)
    while value not in prev_vals:
        try:
            change = next(iterator)
        except StopIteration:
            iterator = iter(changes)
            change = next(iterator)
        prev_vals.append(value)
        value += change
    return value


if __name__ == '__main__':
    with open('input.txt') as f:
        input = f.readlines()
    f = parse_frequency_changes(0, input)
    print(f)

    f = find_repeated_freq(0, input)
    print(f)
