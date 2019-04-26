INPUT = '00111101111101000'
DISK_LENGTH = 272


def expand(data: str) -> str:
    a = data
    b = ''.join(reversed(a))
    b = b.replace('1', '#')
    b = b.replace('0', '1')
    b = b.replace('#', '0')
    return a + '0' + b


def fill_disk(data: str, disk_size: int) -> str:
    while len(data) < disk_size:
        data = expand(data)
    return data[:disk_size]


def checksum(data: str):
    while len(data) % 2 == 0:  # even length
        data = checksum_step(data)
    return data


def checksum_step(data: str):
    cs_list = ['1' if data[i] == data[i+1] else '0' for i in range(0, len(data), 2)]
    return ''.join(cs_list)


def main():
    disk = fill_disk(INPUT, DISK_LENGTH)
    cs = checksum(disk)

    print('Part 1: ', cs)


if __name__ == '__main__':
    main()
