import re

FORBIDDEN_STRINGS = ['i', 'o', 'l']
DOUBLE_LETTER_PATTERN = re.compile(r'([a-z])\1.*([^\\1])\2')


def has_forbidden_letters(password):
    return any([s in password for s in FORBIDDEN_STRINGS])


def has_two_double_letters(password):
    match = DOUBLE_LETTER_PATTERN.search(password)
    return match is not None


def has_straight(password):
    list_ = to_num_list(password)
    for i in range(len(list_)-2):
        if list_[i+1] == list_[i]+1 and list_[i+2] == list_[i]+2:
            return True
    return False


def is_valid(password):
    return (not has_forbidden_letters(password)) and has_straight(password) and has_two_double_letters(password)


def to_num_list(password):
    return [ord(c)-ord('a') for c in password]


def to_string(list_):
    list_ = [chr(num + ord('a')) for num in list_]
    return ''.join(list_)


def increment(list_):
    list_[-1] += 1
    i = -1
    while list_[i] == 26:
        list_[i] = 0
        list_[i-1] += 1
        i -= 1


def get_next_password(old_password):
    password_list = to_num_list(old_password)
    increment(password_list)
    while not is_valid(to_string(password_list)):
        increment(password_list)
    return to_string(password_list)


def main():
    old_password = 'vzbxkghb'
    new_password = get_next_password(old_password)
    print(f'Part 1: Next password is {new_password}')

    new_password = get_next_password(new_password)
    print(f'Part 2: Next password is {new_password}')


if __name__ == '__main__':
    main()
