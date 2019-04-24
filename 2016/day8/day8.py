import numpy as np


class Screen:
    def __init__(self, x: int, y: int):
        self.screen = np.full((y, x), fill_value=0)
        self.command_dict = {'rect': self.rectangle,
                             'rotate': self.rotate}

    def run(self, commands):
        for command_str in commands:
            self.parse_command(command_str)

    def parse_command(self, command_str):
        tokens = command_str.split(' ')
        func = self.command_dict[tokens[0]]
        if func == self.rectangle:
            args = [int(v) for v in tokens[1].split('x')]
        else:
            args = [tokens[2], tokens[4]]  # tokens [3] == 'by'
            if tokens[1] == 'row':
                assert args[0][0:2] == 'y='
            elif tokens[1] == 'column':
                assert args[0][0:2] == 'x='
            else:
                raise ValueError
            args[0] = args[0][2:]
            args = [int(v) for v in args]
            args.insert(0, tokens[1])
        func(*args)

    def rectangle(self, a, b):
        self.screen[0:b, 0:a] = 1

    def rotate(self, dir, index, shift):
        if dir == 'row':
            self.screen[index, :] = np.roll(self.screen[index, :], shift)
        elif dir == 'column':
            self.screen[:, index] = np.roll(self.screen[:, index], shift)
        else:
            raise ValueError

    def __str__(self):
        lst = [''.join([str(e) for e in line])for line in self.screen.tolist()]
        string = '\n'.join(lst)
        string = string.replace('0', '.')
        string = string.replace('1', '#')
        return string

    def checksum(self):
        return sum(sum(self.screen))


def main():
    # screen = Screen(7, 3)
    # commands = ['rect 3x2', 'rotate column x=1 by 1']
    screen = Screen(50, 6)
    with open('day8_input.txt') as file:
        commands = file.readlines()
    commands = [line.strip() for line in commands]
    screen.run(commands)
    print(str(screen))
    print(screen.checksum())
    # answer to part 2 is CFLELOYFCS


if __name__ == '__main__':
    main()
