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


def test_1():
    test_password = 'abcde'
    for i in range(len(test_input)+1):
        yield check_scrambling, test_input[:i], test_password, expected_output[i]


def check_scrambling(instructions, password, expected):
    scrambler = Scrambler(instructions)
    scrambled = scrambler.scramble(password)
    assert scrambled == expected

# Tests of individual functions
# -----------------------------


def test_swap_pos():
    # swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
    password = 'abcde'
    output = Scrambler.swap_pos(password, 1, 2)
    assert output == 'acbde'


def test_swap_letter():
    # swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in
    #   the string).
    password = 'abcde'
    output = Scrambler.swap_letter(password, 'c', 'd')
    assert output == 'abdce'


def test_rotate_steps():
    # rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would
    # turn abcd into dabc.
    password = 'abcde'
    output = Scrambler.rotate(password, -1)
    assert output == 'eabcd'


def test_rotate_letter():
    # rotate based on position of letter X means that the whole string should be rotated to the right based on the index
    #   of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is
    #   determined, rotate the string to the right one time, plus a number of times equal to that index, plus one
    #   additional time if the index was at least 4.
    password = 'abdec'
    output = Scrambler.rotate_letter(password, 'b')
    assert output == 'ecabd'
    output = Scrambler.rotate_letter(output, 'd')
    assert output == 'decab'


def test_reverse():
    # reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X
    # and Y) should be reversed in order.
    password = 'abcdefgh'
    output = Scrambler.reverse(password, 1, 3)
    assert output == 'adcbefgh'
    output = Scrambler.reverse(password, 0, 4)
    assert output == 'edcbafgh'
    output = Scrambler.reverse(password, 5, 7)
    assert output == 'abcdehgf'


def test_move():
    # move position X to position Y means that the letter which is at index X should be removed from the string, then
    # inserted such that it ends up at index Y.
    password = 'abcdefgh'
    output = Scrambler.move(password, 1, 3)
    assert output == 'acdbefgh'
