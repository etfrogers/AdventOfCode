import hashlib


def get_lowest_decimal(key, part2=False):
    i = 0
    while True:
        hasher = hashlib.md5()
        hasher.update((key + str(i)).encode('ascii'))
        hash = hasher.hexdigest()
        if hash[:5] == '00000':
            return i
        i += 1


def main():
    key = 'bgvyzdsv'
    decimal = get_lowest_decimal(key)
    print(f'Part 1: Lowest integer is {decimal}')


if __name__ == '__main__':
    main()
