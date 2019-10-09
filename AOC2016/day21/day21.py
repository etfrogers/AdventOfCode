

class Scrambler:
    def __init__(self, instructions):
        self.instructions = [self.parse_instruction(i) for i in instructions]

    def scramble(self, password):
        for inst in self.instructions:
            func, args = inst
            password = func(password, *args)
        return password

    @staticmethod
    def parse_instruction(instruction):
        words = instruction.split()
        key = ' '.join(words[0:2])
        map_ = FUNCTION_MAPPING[key]
        args = [words[pos] for pos in map_[1]]
        if map_[2]:
            args = [int(v) for v in args]
        return map_[0], tuple(args)

    @staticmethod
    def rotate_letter(input_: str, letter: str):
        # rotate based on position of letter X means that the whole string should be rotated to the right based on
        # the index of letter X (counting from 0) as determined before this instruction does any rotations. Once the
        # index is determined, rotate the string to the right one time, plus a number of times equal to that index,
        # plus one additional time if the index was at least 4.
        index = input_.index(letter)
        steps = index + 1
        if index >= 4:
            steps += 1
        return Scrambler.rotate_right(input_, steps)

    @staticmethod
    def rotate_left(input_: str, steps: int):
        return Scrambler.rotate(input_, steps)

    @staticmethod
    def rotate_right(input_: str, steps: int):
        return Scrambler.rotate(input_, -steps)

    @staticmethod
    def rotate(input_: str, steps: int):
        steps = steps % len(input_)
        return input_[steps:] + input_[:steps]

    @staticmethod
    def swap_letter(password: str, letter_x: str, letter_y: str) -> str:
        # swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they
        # appear in the string).
        return password.translate(str.maketrans(letter_x + letter_y, letter_y + letter_x))

    @staticmethod
    def swap_pos(password: str, pos_x: int, pos_y: int) -> str:
        # swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
        output = list(password)
        output[pos_x] = password[pos_y]
        output[pos_y] = password[pos_x]
        return ''.join(output)

    @staticmethod
    def reverse(password: str, pos_x: int, pos_y: int):
        # reverse positions X through Y means that the span of letters at indexes X through Y (including the letters
        # at X and Y) should be reversed in order.
        assert pos_x <= pos_y
        if pos_x == 0:
            mid = password[pos_y::-1]
        else:
            mid = password[pos_y:pos_x - 1:-1]
        return password[:pos_x] + mid + password[pos_y+1:]

    @staticmethod
    def move(password: str, pos_x: int, pos_y: int):
        # move position X to position Y means that the letter which is at index X should be removed from the string,
        # then inserted such that it ends up at index Y.
        output = list(password)
        output.insert(pos_y, output.pop(pos_x))
        return ''.join(output)


# swap position X with position Y
# swap letter X with letter Y
# rotate left/right X steps
# rotate based on position of letter X
# reverse positions X through Y
# move position X to position Y
FUNCTION_MAPPING = {'swap position': (Scrambler.swap_pos, (2, 5), True),
                    'swap letter': (Scrambler.swap_letter, (2, 5), False),
                    'rotate left': (Scrambler.rotate_left, (2, ), True),
                    'rotate right': (Scrambler.rotate_right, (2, ), True),
                    'rotate based': (Scrambler.rotate_letter, (6, ), False),
                    'reverse positions': (Scrambler.reverse, (2, 4), True),
                    'move position': (Scrambler.move, (2, 5), True),
                    }


def main():
    password = 'abcdefgh'
    with open('input.txt') as f:
        instructions = f.readlines()
    scrambler = Scrambler(instructions)
    scrambled = scrambler.scramble(password)
    print('Part 1: Scrambled password is ', scrambled)


if __name__ == '__main__':
    main()
