import math
from collections import defaultdict
from typing import List, Tuple, Union
import numpy as np

from utils import Point, Directions, Direction, array_to_string
from intcode import IntCodeComputer


def main():
    comp = IntCodeComputer('input.txt', [])
    bot = PaintBot(comp)
    bot.build_panels(debug=False)
    # print(bot.render())
    print(f'Total number of panels visited: {len(bot.panels)}')

    comp = IntCodeComputer('input.txt', [])
    bot = PaintBot(comp, initial_color=1)
    bot.build_panels()
    print(bot.render())
    # Identifier is GARPKZUL


class PaintBot:
    bot_chars = {Directions.NORTH.tuple: '^',
                 Directions.SOUTH.tuple: 'v',
                 Directions.EAST.tuple: '>',
                 Directions.WEST.tuple: '<',
                 }

    def __init__(self, comp: IntCodeComputer = None, fake_data: List[Tuple[int, int]] = None, initial_color: int = 0):
        self.comp = comp
        self.fake_data = fake_data
        if fake_data is not None:
            self.fake_input = []
        self.panels = defaultdict(int)
        self.location = Point(0, 0)
        self.panels[self.location.tuple] = initial_color
        self.direction = Directions.NORTH

    def build_panels(self, debug=False):
        while (self.comp and not self.comp.finished) or self.fake_data:
            input_ = self.panels[self.location.tuple]
            if self.comp:
                self.comp.input_data.push(input_)
                self.comp.resume()
                data = (self.comp.output_data.pop(), self.comp.output_data.pop())
                assert len(self.comp.output_data) == 0
            elif self.fake_data is not None:
                self.fake_input.append(input_)
                data = self.fake_data.pop(0)
            else:
                raise ValueError
            color, turn_direction = data
            assert color in (0, 1)
            assert turn_direction in (0, 1)

            self.panels[self.location.tuple] = color
            self.turn(self.direction, turn_direction)
            self.location.move(self.direction)
            if debug:
                print(self.render() + '\n---')
                pass

    @staticmethod
    def turn(direction: Direction, turn_direction: int):
        if turn_direction == 0:
            direction.turn_left()
        elif turn_direction == 1:
            direction.turn_right()
        else:
            raise ValueError

    def render(self, override_size=None) -> str:
        if override_size:
            corner = math.floor(override_size/2)
            bottom_left = Point(-corner, -corner)
            top_right = Point(corner, corner)
        else:
            xs, ys = zip(*self.panels.keys())
            xs += (self.location.x, )
            ys += (self.location.y, )
            bottom_left = Point(min(xs), min(ys))
            top_right = Point(max(xs), max(ys))

        def _to_np_coords(pt: Union[Point, Tuple[int, int]]):
            try:
                out = pt - bottom_left
            except TypeError:
                out = Point(*pt) - bottom_left
            return tuple(reversed(out.tuple))
        size = _to_np_coords(top_right + Point(1, 1))
        map_ = np.zeros(size, dtype=int)
        for key, value in self.panels.items():
            map_[_to_np_coords(key)] = value
        render_map = {0: '.', 1: '#'}
        string = array_to_string(map_, render_map,
                                 overrides=[(_to_np_coords(self.location), self.bot_chars[self.direction.tuple])])
        return string


def paint_execute(initial_color=0):
    """From Reddit"""
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    program = IntCodeComputer('input.txt', [])
    x = y = direction = 0
    panel = { (x, y): initial_color }
    while not program.finished:
        program.input_data.append(panel[(x, y)] if (x, y) in panel else 0)
        program.resume()
        # output2 = program.run()
        output1, output2 = program.output_data
        program.output_data = []
        if not program.finished:
            panel[(x, y)] = output1
            direction = ((direction + 1) if output2 == 1 else (direction - 1 + len(directions))) % len(directions)
            x, y = x + directions[direction][0], y + directions[direction][1]
    return panel


if __name__ == '__main__':
    main()
    # panel = paint_execute(0)
    # print(len(panel))
