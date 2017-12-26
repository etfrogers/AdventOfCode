
class Dancers:
    def __init__(self, length):
        self._formation = [chr(ord('a') + v) for v in range(0, length)]
        self.move_dict = {'s': {'func': self.spin, 'nargs': 1, 'conv': int},
                          'x': {'func': self.exchange, 'nargs': 2, 'conv': int},
                          'p': {'func': self.partner, 'nargs': 2, 'conv': lambda x: x}}

    @property
    def formation(self):
        return ''.join(self._formation)

    def spin(self, n):
        self._formation = self._formation[-n:] + self._formation[:len(self._formation) - n]

    def exchange(self, i1, i2):
        self._formation[i1], self._formation[i2] = self._formation[i2], self._formation[i1]

    def partner(self, p1, p2):
        self.exchange(self._formation.index(p1), self._formation.index(p2))

    def do_move(self, move):
        move_char = move[0]
        args = move[1:].split('/')

        move_data = self.move_dict[move_char]
        args = [move_data['conv'](a) for a in args]
        move_data['func'](*args)

    def perform(self, moves):
        [self.do_move(move) for move in moves]


def main():
    with open('input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = dance_moves.split(',')
    dancers = Dancers(16)

    dancers.perform(dance_moves)
    print(dancers.formation)


if __name__ == '__main__':
    main()
