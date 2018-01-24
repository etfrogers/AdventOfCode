import hashlib


def get_next_char(door_id, part2=False):
    i = 0
    while True:
        hasher = hashlib.md5()
        hasher.update((door_id + str(i)).encode('ascii'))
        hash = hasher.hexdigest()
        if hash[:5] == '00000':
            if part2:
                try:
                    pos = int(hash[5])
                except ValueError:
                    pass
                char = hash[6]
                if pos < 8:
                    yield pos, char
            else:
                yield hash[5]
        i += 1


def get_password(door_id, part2=False):
    pw_chars = get_next_char(door_id, part2)
    if part2:
        pw = ['*' for _ in range(8)]
        while '*' in pw:
            pos, char = pw_chars.__next__()
            if pw[pos] == '*':
                pw[pos] = char
            print(pw)
    else:
        pw = []
        while len(pw) < 8:
            pw.append(pw_chars.__next__())
            print(pw)
    return ''.join(list(pw))


def main():
    pw = get_password('uqwqemis', part2=True)
    # pw = get_password('abc', part2=True)
    print(pw)


if __name__ == '__main__':
    main()