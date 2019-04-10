from enum import IntEnum, Enum
from typing import List, Tuple

import numpy as np


class CartTurnDir(IntEnum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

    def next(self):
        return CartTurnDir((self.value + 1) % 3)


class Direction(Enum):
    # format is y, x as used by numpy
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

    @property
    def coords(self):
        return np.array(self.value)

    def direction_after_turn(self, turn_direction):
        list_of_dirs = list(Direction)
        curr_index = list_of_dirs.index(self)
        if turn_direction == CartTurnDir.LEFT:
            curr_index -= 1
        elif turn_direction == CartTurnDir.RIGHT:
            curr_index += 1
            curr_index %= len(list_of_dirs)
        elif turn_direction == CartTurnDir.STRAIGHT:
            pass
        else:
            raise ValueError
        return list_of_dirs[curr_index]


class Cart:
    symbols = {'^': (Direction.NORTH, '|'),
               '>': (Direction.EAST, '-'),
               'v': (Direction.SOUTH, '|'),
               '<': (Direction.WEST, '-')}

    direction_changes = {(Direction.NORTH, '|'): Direction.NORTH,
                         (Direction.NORTH, '/'): Direction.EAST,
                         (Direction.NORTH, '\\'): Direction.WEST,
                         (Direction.SOUTH, '|'): Direction.SOUTH,
                         (Direction.SOUTH, '/'): Direction.WEST,
                         (Direction.SOUTH, '\\'): Direction.EAST,
                         (Direction.WEST, '-'): Direction.WEST,
                         (Direction.WEST, '/'): Direction.SOUTH,
                         (Direction.WEST, '\\'): Direction.NORTH,
                         (Direction.EAST, '-'): Direction.EAST,
                         (Direction.EAST, '/'): Direction.NORTH,
                         (Direction.EAST, '\\'): Direction.SOUTH,
                         }

    symbol_finder = {i[0]: s for s, i in symbols.items()}

    def __init__(self, coords, symbol):
        self.coords = coords
        self.direction = self.symbols[symbol][0]
        self.turn_direction = CartTurnDir.LEFT

    @property
    def symbol(self):
        return self.symbol_finder[self.direction]

    @property
    def reading_order(self):
        return self.coords[0], self.coords[1]

    def tick(self, map_):
        self.move()
        self.update_direction(map_)

    def move(self):
        self.coords += self.direction.coords

    @property
    def numpy_coords(self):
        return tuple(self.coords)

    def update_direction(self, map_):
        current_symbol = map_[self.numpy_coords]
        if current_symbol == '+':
            self.direction = self.direction.direction_after_turn(self.turn_direction)
            self.turn_direction = self.turn_direction.next()
        else:
            self.direction = self.direction_changes[(self.direction, current_symbol)]


class Track:
    def __init__(self, input_map: List[str], crash_removal: bool=False):
        self.map, self.carts = self.extract_carts(input_map)
        self.collision = None
        self.crash_removal = crash_removal

    def render_map(self):
        return '\n'.join([''.join(line) for line in self.map.tolist()])

    def render(self):
        map_ = self.map.copy()
        for cart in self.carts:
            map_[cart.numpy_coords] = cart.symbol
        if self.collision and not self.crash_removal:
            map_[self.collision] = 'X'
        return '\n'.join([''.join(line) for line in map_])

    @staticmethod
    def extract_carts(input_map: List[str]) -> Tuple[np.ndarray, List[Cart]]:
        map_ = np.array([list(line) for line in input_map])
        coord_arrays = tuple(map_ == symbol for symbol in Cart.symbols.keys())
        cart_coords = np.transpose(np.logical_or.reduce(coord_arrays).nonzero())
        cart_coords = [tuple(coords) for coords in cart_coords]
        carts = [Cart(coords, map_[coords]) for coords in cart_coords]
        for symbol, info in Cart.symbols.items():
            map_[map_ == symbol] = info[1]
        return map_, carts

    def tick(self):
        sorted_carts = sorted(self.carts, key=lambda x: x.reading_order)
        for cart in sorted_carts:
            cart.tick(self.map)
            self.check_for_collisions(cart)
        if len(self.carts) == 1:
            raise LastCartException(self.carts[0].numpy_coords)

    def check_for_collisions(self, other):
        for cart in self.carts.copy():
            if np.all(cart.coords == other.coords) and cart is not other:
                self.collision = cart.numpy_coords
                if self.crash_removal:
                    self.carts.remove(cart)
                    self.carts.remove(other)
                    assert len(self.carts) > 0
                else:
                    raise CollisionException(cart.numpy_coords)

    def evolve(self):
        while True:
            try:
                self.tick()
            except (CollisionException, LastCartException) as err:
                return err.coords

    @staticmethod
    def format_coords(coords):
        return f'{coords[1]},{coords[0]}'


class TrackException(Exception):
    def __init__(self, coords, *args):
        super().__init__(*args)
        self.coords = coords


class CollisionException(TrackException):
    pass


class LastCartException(TrackException):
    pass


def main():
    with open('input.txt') as file:
        input_ = file.readlines()
    input_ = [line.replace('\n', '') for line in input_]
    track = Track(input_)
    collision = track.evolve()
    print(f'Part 1: {track.format_coords(collision)}')

    track = Track(input_, crash_removal=True)
    last_cart = track.evolve()
    print(f'Part 2: {track.format_coords(last_cart)}')


if __name__ == '__main__':
    main()
