from collections import Counter
from time import sleep
from typing import Union

from intcode import IntCodeComputer
from utils import Point, coord_map_to_array, array_to_string


class Game:
    def __init__(self, comp: IntCodeComputer):
        self.comp: IntCodeComputer = comp
        self.tiles: dict = {}
        self.score: Union[int, None] = None

    def calc_new_frame(self):
        self.comp.resume()
        while self.comp.output_data:
            x, y, tile_id = self.comp.get_output(3)
            point = Point(x, y)
            if point.tuple == (-1, 0):
                self.score = tile_id
                continue
            self.tiles[point.tuple] = tile_id

    def render(self):
        array = coord_map_to_array(self.tiles)
        map_ = {0: ' ', 1: '#', 2: '*', 3: '-', 4: 'O'}
        string = array_to_string(array, map_, flip=False)
        print(string)
        if self.score is not None:
            print(f'Score: {self.score}')

    def set_joystick(self):
        if not self.tiles:
            return
        ball_x, _ = self.get_ball()
        paddle_x, _ = self.get_paddle()
        if paddle_x < ball_x:
            value = 1
        elif paddle_x > ball_x:
            value = -1
        else:
            value = 0
        self.comp.input_data.push(value)

    def get_tile(self, value):
        return list(self.tiles.keys())[list(self.tiles.values()).index(value)]

    def get_ball(self):
        return self.get_tile(4)

    def get_paddle(self):
        return self.get_tile(3)


def main():
    comp = IntCodeComputer('input.txt', [])
    game = Game(comp)
    game.calc_new_frame()
    game.render()
    count = Counter(game.tiles.values())
    n_blocks = count[2]
    print(f'Number of blocks is {n_blocks}')

    # Part 2
    comp = IntCodeComputer('input.txt', [])
    comp.instructions[0] = 2
    game = Game(comp)
    while not game.comp.finished:
        game.set_joystick()
        game.calc_new_frame()
        # game.render()
        # sleep(0.1)
    print(f'Final score: {game.score}')


if __name__ == '__main__':
    main()
