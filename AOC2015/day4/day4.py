import hashlib


def get_lowest_decimal(key, part2=False):
    i = 0
    while True:
        hasher = hashlib.md5()
        hasher.update((key + str(i)).encode('ascii'))
        hash = hasher.hexdigest()
        if part2:
            length = 6
        else:
            length = 5
        if hash[:length] == '0'*length:
            return i
        i += 1


def main():
    key = 'bgvyzdsv'
    decimal = get_lowest_decimal(key)
    print(f'Part 1: Lowest integer is {decimal}')

    decimal = get_lowest_decimal(key, part2=True)
    print(f'Part 2: Lowest integer is {decimal}')


if __name__ == '__main__':
    main()
