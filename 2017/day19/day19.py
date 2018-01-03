

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


class Direction(Point):
    def __init__(self, x, y):
        assert abs(x) + abs(y) == 1
        assert x == 0 or y == 0
        super().__init__(x, y)

    def get_hv(self):
        if self.x == 0:
            return 'v'
        elif self.y == 0:
            return 'h'


class Diagram:
    def __init__(self, diagram):
        self.data = diagram

    def __getitem__(self, item):
        if item.y < 0 or item.y >= len(self.data):
            return '.'
        if item.x < 0 or item.x >= len(self.data[item.y]):
            return '.'
        return self.data[item.y][item.x]

    def find_start(self):
        x_coord = self.data[0].index('|')
        return Point(x_coord, 0)

    def walk(self, start_point, direction):
        pt = start_point
        curr_dir = direction
        letter_stack = []
        letters = [chr(v) for v in range(ord('A'), ord('Z')+1)]
        finished = False
        while not finished:
            pt = pt + curr_dir
            char = self[pt]
            # print(char)
            if char in letters:
                letter_stack.append(char)
            elif char == '+':
                if curr_dir.get_hv() == 'h':
                    # look above and below
                    if self[pt + Direction(0, 1)] in letters + ['|']:
                        curr_dir = Direction(0, 1)
                    if self[pt + Direction(0, -1)] in letters + ['|']:
                        curr_dir = Direction(0, -1)
                elif curr_dir.get_hv() == 'v':
                    # look left and right
                    if self[pt + Direction(1, 0)] in letters + ['-']:
                        curr_dir = Direction(1, 0)
                    if self[pt + Direction(-1, 0)] in letters + ['-']:
                        curr_dir = Direction(-1, 0)

            # change_dir
            elif char == ' ':
                finished = True
        return letter_stack

    def __str__(self):
        return '\n'.join(self.data)


def main():
    with open('input.txt', 'r') as file:
        diagram = file.readlines()
    diagram = [line.strip('\n') for line in diagram]
    diagram = Diagram(diagram)
    pt = diagram.find_start()
    direction = Direction(0, 1)
    print(diagram)
    letter_stack = diagram.walk(pt, direction)
    print(''.join(letter_stack))


if __name__ == '__main__':
    main()
