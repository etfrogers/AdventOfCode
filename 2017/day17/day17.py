
def calc_spinlock(n, step):
    pos = 0
    buffer = [0]
    done = False
    val_to_insert = 1
    # print(buffer)
    while not done:
        new_pos = (pos + step) % len(buffer)
        # print(new_pos)
        buffer.insert(new_pos+1, val_to_insert)
        val_to_insert += 1
        # print(buffer)
        pos = new_pos + 1
        done = val_to_insert > n
    value = buffer[pos+1]
    return value, buffer


def main():
    step = 349
    n = 2017
    value, buffer = calc_spinlock(n, step)
    print(value)


if __name__ == '__main__':
    main()
