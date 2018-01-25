from collections import Counter


def unscramble(scrambled, modified=False):
    scr_list = [list(line.strip()) for line in scrambled]
    scr_stream = zip(*scr_list)
    if modified:
        plaintext = [Counter(col).most_common()[-1][0] for col in scr_stream]
    else:
        plaintext = [Counter(col).most_common(1)[0][0] for col in scr_stream]
    return ''.join(plaintext)


def main():
    with open('day6_input.txt') as file:
        scrambled = file.readlines()
    plaintext = unscramble(scrambled, True)
    print(plaintext)


if __name__ == '__main__':
    main()