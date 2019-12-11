def two_digits_same(password, part2):
    dp = diff(password)
    if part2:
        ddp = diff(dp)
        ddp = [-1] + ddp + [-1]
        candidates = [i for i in range(len(dp)) if dp[i] == 0]
        if not candidates:
            valid = False
        else:
            valid = False
            for candidate in candidates:
                if ddp[candidate] != 0 and ddp[candidate+1] != 0:
                    valid = True
        return valid
    else:
        return any([d == 0 for d in dp])


def diff(password):
    return [int(password[i+1]) - int(password[i]) for i in range(len(password)-1)]


def non_decreasing(password):
    return all([d >= 0 for d in diff(password)])


def is_valid(password, part2=False):
    return len(password) == 6 and two_digits_same(password, part2) and non_decreasing(password)


def main():
    input_ = (236491, 713787)
    counter1 = counter2 = 0
    for i in range(input_[0], input_[1] + 1):
        password = str(i)
        if is_valid(password):
            counter1 += 1
        if is_valid(password, part2=True):
            counter2 += 1
    print(f'Number of valid passwords part 1: {counter1}')
    print(f'Number of valid passwords part 2: {counter2}')


if __name__ == '__main__':
    main()
