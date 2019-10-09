from AOC2016.day21.day21 import Scrambler

test_input = ['swap position 4 with position 0',
              'swap letter d with letter b',
              'reverse positions 0 through 4',
              'rotate left 1 step',
              'move position 1 to position 4',
              'move position 3 to position 0',
              'rotate based on position of letter b',
              'rotate based on position of letter d']

expected_output = ['abcde',
                   'ebcda',
                   'edcba',
                   'abcde',
                   'bcdea',
                   'bdeac',
                   'abdec',
                   'ecabd',
                   'decab']


def test_scrambling():
    test_password = 'abcde'
    for i in range(len(test_input)+1):
        yield check_scrambling, test_input[:i], test_password, expected_output[i]


def test_unscrambling():
    test_password = 'abcde'
    for i in range(len(test_input)+1):
        yield check_unscrambling, test_input[:i], test_password, expected_output[i]


def check_scrambling(instructions, password, expected):
    scrambler = Scrambler(instructions)
    scrambled = scrambler.scramble(password)
    assert scrambled == expected


def check_unscrambling(instructions, password, scrambled_password):
    scrambler = Scrambler(instructions)
    unscrambled = scrambler.unscramble(scrambled_password)
    assert unscrambled == password


# Tests of individual functions
# -----------------------------


def test_swap_pos():
    # swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
    password = 'abcde'
    output = Scrambler.swap_pos(password, 1, 2, invert=False)
    assert output == 'acbde'


def test_swap_letter():
    # swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in
    #   the string).
    password = 'abcde'
    output = Scrambler.swap_letter(password, 'c', 'd', _=False)
    assert output == 'abdce'


def test_rotate_steps():
    # rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would
    # turn abcd into dabc.
    password = 'abcde'
    output = Scrambler.rotate(password, -1, invert=False)
    assert output == 'eabcd'


def test_rotate_letter():
    # rotate based on position of letter X means that the whole string should be rotated to the right based on the index
    #   of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is
    #   determined, rotate the string to the right one time, plus a number of times equal to that index, plus one
    #   additional time if the index was at least 4.
    password = 'abdec'
    output = Scrambler.rotate_letter(password, 'b', invert=False)
    assert output == 'ecabd'
    output = Scrambler.rotate_letter(output, 'd', invert=False)
    assert output == 'decab'


def test_reverse():
    # reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X
    # and Y) should be reversed in order.
    password = 'abcdefgh'
    output = Scrambler.reverse(password, 1, 3, _=False)
    assert output == 'adcbefgh'
    output = Scrambler.reverse(password, 0, 4, _=False)
    assert output == 'edcbafgh'
    output = Scrambler.reverse(password, 5, 7, _=False)
    assert output == 'abcdehgf'


def test_move():
    # move position X to position Y means that the letter which is at index X should be removed from the string, then
    # inserted such that it ends up at index Y.
    password = 'abcdefgh'
    output = Scrambler.move(password, 1, 3, invert=False)
    assert output == 'acdbefgh'


def test_part1():
    password = 'abcdefgh'
    with open('input.txt') as f:
        instructions = f.readlines()
    scrambler = Scrambler(instructions)
    scrambled = scrambler.scramble(password)
    assert scrambled == 'baecdfgh'


def test_part2():
    scrambled = 'fbgdceah'

    with open('input.txt') as f:
        instructions = f.readlines()
    scrambler = Scrambler(instructions)

    unscrambled = scrambler.unscramble(scrambled)
    assert unscrambled == 'cegdahbf'
