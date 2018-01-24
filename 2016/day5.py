import hashlib


def get_next_char(door_id):
    i = 0
    while True:
        hasher = hashlib.md5()
        hasher.update((door_id + str(i)).encode('ascii'))
        hash = hasher.hexdigest()
        if hash[:5] == '00000':
            yield hash[5]
        i += 1


def get_password(door_id):
    pw = []
    pw_chars = get_next_char(door_id)
    while len(pw) < 8:
        pw.append(pw_chars.__next__())
        print(pw)
    return ''.join(list(pw))


def main():
    pw = get_password('uqwqemis')
    print(pw)


if __name__ == '__main__':
    main()