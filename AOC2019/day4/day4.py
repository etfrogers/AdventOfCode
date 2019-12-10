def two_digits_same(password):
    return any([d == 0 for d in diff(password)])


def diff(password):
    return [int(password[i+1]) - int(password[i]) for i in range(len(password)-1)]


def non_decreasing(password):
    return all([d >= 0 for d in diff(password)])


def is_valid(password):
    return len(password) == 6 and two_digits_same(password) and non_decreasing(password)


def main():
    input_ = (236491, 713787)
    counter = 0
    for i in range(input_[0], input_[1] + 1):
        password = str(i)
        if is_valid(password):
            counter += 1
    print(f'Number of valid passwords: {counter}')


if __name__ == '__main__':
    main()
