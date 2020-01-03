from typing import List, Union

from AOC2019.day9.day9 import RelativeIntCodeComputer
from utils import FIFOQueue


class IntCodeComputer(RelativeIntCodeComputer):
    def __init__(self, instructions, input_=None):
        try:
            with open(instructions) as file:
                instructions = file.read().strip()
        except FileNotFoundError:
            pass
        super().__init__(instructions, input_)

    def get_output(self, n: int = 1, all_elements: bool = False) -> Union[int, List[int]]:
        if all_elements:
            assert n == 1, ValueError('If all_elements is specified, n must not be')
            lst = list(self.output_data)
            self.output_data = FIFOQueue([])
            return lst
        elif n < 0 or n > len(self.output_data):
            raise IndexError('Invalid number of elements specified')
        else:
            return [self.output_data.pop() for _ in range(n)]
