from collections import Counter


def is_valid(password_line: str):
    letter, min_counts, max_counts, password = parse_line(password_line)
    counter = Counter(password)
    counts = counter[letter]
    return min_counts <= counts <= max_counts


def is_valid2(password_line: str):
    letter, first_position, second_position, password = parse_line(password_line)
    # subtract one because puzzle is one-indexed, python is zero-indexed
    return (password[first_position-1] == letter) ^ (password[second_position-1] == letter)


def parse_line(password_line):
    rule, password = password_line.split(': ')
    counts, letter = rule.split(' ')
    min_counts, max_counts = counts.split('-')
    min_counts = int(min_counts)
    max_counts = int(max_counts)
    return letter, min_counts, max_counts, password


def number_of_valid_passwords(password_list, part2=False):
    count = 0
    for line in password_list:
        if part2:
            if is_valid2(line):
                count += 1
        else:
            if is_valid(line):
                count += 1
    return count


def main():
    with open('input.txt') as file:
        password_list = file.readlines()
    password_list = [line.strip() for line in password_list]
    n = number_of_valid_passwords(password_list)
    print(f'Part 1: Number of valid passwords: {n}')

    n = number_of_valid_passwords(password_list, part2=True)
    print(f'Part 2: Number of valid passwords: {n}')


if __name__ == '__main__':
    main()