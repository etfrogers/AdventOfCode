
def find_floor(string):
    return string.count('(') - string.count(')')


def find_first_basement(string: str):
    for i in range(len(string)):
        if find_floor(string[:i]) < 0:
            return i


def main():
    with open('input.txt') as f:
        input_ = f.readline()
    floor = find_floor(input_)
    print(f'Part 1: floor {floor}')
    floor2 = find_first_basement(input_)
    print(f'Part 1: Character {floor2}')


if __name__ == '__main__':
    main()