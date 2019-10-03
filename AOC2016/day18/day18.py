
TRAP = '^'
SAFE = '.'


class Room:
    def __init__(self, first_row: str, n_rows: int):
        self.rows = [first_row]
        for i in range(1, n_rows):
            self.rows.append(self.build_row(self.rows[i-1]))

    def render(self) -> str:
        return '\n'.join(self.rows)

    @staticmethod
    def build_row(old_row: str) -> str:
        new_row = list(SAFE * len(old_row))
        for pos in range(len(old_row)):
            left = SAFE if pos == 0 else old_row[pos-1]
            centre = old_row[pos]
            right = SAFE if pos == len(old_row)-1 else old_row[pos+1]
            if (left == centre == TRAP and right == SAFE) or \
               (centre == right == TRAP and left == SAFE) or \
               (left == TRAP and right == centre == SAFE) or \
               (right == TRAP and left == centre == SAFE):
                new_row[pos] = TRAP

        return ''.join(new_row)

    @property
    def n_safe_squares(self):
        return sum([1 for c in self.render() if c == SAFE])


def main():
    first_row = '.^..^....^....^^.^^.^.^^.^.....^.^..^...^^^^^^.^^^^.^.^^^^^^^.^^^^^..^.^^^.^^..^.^^.^....^.^...^^.^.'
    n_rows = 40

    room = Room(first_row, n_rows)
    print('Part 1: Number of safe squares = ', room.n_safe_squares)


if __name__ == '__main__':
    main()
