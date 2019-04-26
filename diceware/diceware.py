import argparse
import secrets

DICEWARE_ROLLS = 5
DICEWARE_FILE = 'diceware.wordlist.asc'
DICEWARE_DICT = None  # loaded below


def load_diceware_list():
    with open(DICEWARE_FILE) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = lines[2:-11]  # drop header and footer
    diceware = {l.split('\t')[0]: l.split('\t')[1] for l in lines}
    assert len(diceware) == 6**5
    return diceware


def dice_roll() -> int:
    return secrets.randbelow(6) + 1


def generate_key() -> str:
    ints = [dice_roll() for _ in range(DICEWARE_ROLLS)]
    return ''.join([str(i) for i in ints])


def generate_password(n: int, spaces: bool) -> str:
    keys = [generate_key() for _ in range(n)]
    words = [DICEWARE_DICT[key] for key in keys]
    joiner = ' ' if spaces else ''
    password = joiner.join(words)
    return password


DICEWARE_DICT = load_diceware_list()


def main():
    parser = argparse.ArgumentParser(description='Produce a diceware password.')
    parser.add_argument('--length', '-n', type=int, default=6,
                        help='The number of words in the generated password. Default is 6')
    parser.add_argument('--no-spaces', '-s', action='store_const', const=True, default=False,
                        help='If this argument is given, do not separate the words in the password with spaces')

    args = parser.parse_args()

    password = generate_password(args.length, not args.no_spaces)
    print(password)


if __name__ == '__main__':
    main()
