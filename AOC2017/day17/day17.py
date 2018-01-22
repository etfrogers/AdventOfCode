
def calc_spinlock(n, step):
    pos = 0
    buffer = [0]
    done = False
    val_to_insert = 1
    pos_list = []
    while not done:
        new_pos = (pos + step) % len(buffer)
        buffer.insert(new_pos+1, val_to_insert)
        val_to_insert += 1
        pos_list.append(pos)
        pos = new_pos + 1
        done = val_to_insert > n
    print(pos_list)
    value = buffer[pos+1]
    return value, buffer


def spinlock_track_0(n, step):
    pos = 1
    pos_0 = 0
    val_after_0 = 1
    length = 2
    for val in range(2, n + 1):
        pos = ((pos + step) % length) + 1
        if pos == (pos_0 + 1) % length:
            val_after_0 = val
        if pos <= pos_0:
            pos_0 += 1
        length += 1
        if val % 100000 == 0:
            print(val)
    return val_after_0


def main():
    step = 349
    n = 50000000
    value0 = spinlock_track_0(n, step)

    print(value0)


if __name__ == '__main__':
    main()
