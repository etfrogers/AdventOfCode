from collections import Counter


def unscramble(scrambled):
    scr_list = [list(line.strip()) for line in scrambled]
    scr_stream = zip(*scr_list)
    plaintext = [Counter(col).most_common(1)[0][0] for col in scr_stream]
    return ''.join(plaintext)


def main():
    with open('day6_input.txt') as file:
        scrambled = file.readlines()
    plaintext = unscramble(scrambled)
    print(plaintext)


if __name__ == '__main__':
    main()