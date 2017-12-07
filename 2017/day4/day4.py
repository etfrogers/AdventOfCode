
def is_valid(passphrase, with_anagrams=False):
    token_list = passphrase.split(' ')
    if with_anagrams:
        token_list = [''.join(sorted(token)) for token in token_list]
    token_set = set(token_list)
    print(passphrase)
    print('%d tokens found, %d unique' % (len(token_list), len(token_set)))
    return len(token_list) == len(token_set)


def count_valid_phrases(phraselist, with_anagrams=False):
    valid_list = [is_valid(phrase, with_anagrams) for phrase in phraselist]
    return sum(valid_list)


def main():
    with open('input.txt', 'r') as file:
        phrase_list = file.readlines()
    phrase_list = [line.strip() for line in phrase_list]
    count = count_valid_phrases(phrase_list, True)
    print('%d of %d are valid' % (count, len(phrase_list)))


if __name__ == '__main__':
    main()