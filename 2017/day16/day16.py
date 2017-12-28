from enum import Enum


class Speed(Enum):
    SLOW = 0
    FASTER = 1
    FASTEST = 2


class Dancers:
    def __init__(self, length, start_char='a'):
        self._length = length
        self._start_char = start_char
        self._formation = self.char_list()
        self.move_dict = {'s': {'func': self.spin, 'nargs': 1, 'conv': int},
                          'x': {'func': self.exchange, 'nargs': 2, 'conv': int},
                          'p': {'func': self.partner, 'nargs': 2, 'conv': lambda x: x}}
        self.reposition = None

    def char_list(self):
        return [chr(ord(self._start_char) + v) for v in range(0, self._length)]

    def reset(self):
        self._formation = self.char_list()

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

    def store_reposition(self):
        self.reposition = [self.char_list().index(c) for c in self._formation]
        print(self.reposition)

    def apply_reposition(self):
        if self.reposition is None:
            raise AttributeError
        else:
            # self._formation = [self._formation[i] for i in self.reposition]
            print('-------------------')
            print('Applying reposition')
            print('State before')
            print(self.formation)
            for j, i in enumerate(self.reposition):
                print('%d - %d: %s' % (j, i, self._formation[i]))
            self._formation = [self._formation[i] for i in self.reposition]
            print('State after')
            print(self.formation)
            print('Finished reposition')
            print('-------------------')

    def whole_dance(self, moves, reps, speed=Speed.FASTEST):
        self.reset()
        if speed == speed.SLOW:
            for _ in range(reps):
                self.perform(moves)
            return None

        self.perform(moves)
        self.store_reposition()
        self.reset()

        configs = []
        for i in range(0, reps):
            self.apply_reposition()
            if speed == Speed.FASTEST:
                if self.formation in configs:
                    break
                configs.append(self.formation)
            # if i % 10000 == 0:
        if speed == Speed.FASTER:
            return None
        else:  # speed = Speed.FASTEST
            pre_len = configs.index(self.formation)
            #print(pre_len)
            loop_len = len(configs)-pre_len
            remainder = (reps - pre_len) % loop_len

            self._formation = configs[remainder]
            # print(self.formation)


def main():
    reps = int(1e9)
    reps = int(1e6)
    with open('test_input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = dance_moves.split(',')
    dancers = Dancers(5, 'a')

    reps = 50
    dancers.whole_dance(dance_moves, reps, Speed.SLOW)
    slow_formation = dancers.formation
    print(slow_formation)
    dancers.store_reposition()
    print(dancers.reposition)
    dancers.whole_dance(dance_moves, reps, Speed.FASTER)
    faster_formation = dancers.formation
    print(faster_formation)


if __name__ == '__main__':
    main()
