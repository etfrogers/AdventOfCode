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
    NORTH = (0, 1)
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)


class Cart:
    symbols = {'^': (Direction.NORTH, '|'),
               '>': (Direction.EAST, '-'),
               'v': (Direction.SOUTH, '|'),
               '<': (Direction.WEST, '-')}

    def __init__(self, coords, symbol):
        self.coords = coords
        self.direction = self.symbols[symbol][0]


class Track:
    def __init__(self, input_map: List[str]):
        self.map, self.carts = self.extract_carts(input_map)

    def render_map(self):
        return [''.join(line) for line in self.map.tolist()]

    @staticmethod
    def extract_carts(input_map: List[str]) -> Tuple[np.ndarray, List[Cart]]:
        map_ = np.array([line.split() for line in input_map])
        coord_arrays = tuple(map_ == symbol for symbol in Cart.symbols.keys())
        cart_coords = np.transpose(np.logical_or.reduce(coord_arrays).nonzero())
        cart_coords = [tuple(coords) for coords in cart_coords]
        carts = [Cart(coords, map_[coords]) for coords in cart_coords]
        for symbol, info in Cart.symbols.items():
            map_[map_ == symbol] = info[1]
        return map_, carts
