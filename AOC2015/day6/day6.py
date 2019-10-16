import numpy as np


class Lights:
    def __init__(self, size=1000):
        self.lights = np.zeros((size, size), dtype=int)

    def process_instructions(self, instructions):
        for instruction in instructions:
            action, start_points, end_points = self.parse_instruction(instruction)
            x_slice = slice(start_points[0], end_points[0]+1)
            y_slice = slice(start_points[1], end_points[1]+1)
            if action == 'on':
                self.lights[x_slice, y_slice] = 1
            elif action == 'off':
                self.lights[x_slice, y_slice] = 0
            elif action == 'toggle':
                self.lights[x_slice, y_slice] = \
                    abs(self.lights[x_slice, y_slice] - 1)
            else:
                raise ValueError

    @staticmethod
    def parse_instruction(instruction):
        tokens = instruction.split()
        end_points = Lights.to_coords(tokens[-1])
        assert tokens[-2] == 'through'
        start_points = Lights.to_coords(tokens[-3])
        action = tokens[-4]
        return action, start_points, end_points

    @staticmethod
    def to_coords(string):
        return tuple(int(v) for v in string.split(','))

    @property
    def number_lit(self):
        return np.sum(self.lights)


def main():
    with open('input.txt') as f:
        instructions = f.readlines()
    lights = Lights()
    lights.process_instructions(instructions)
    print(f'Part 1: Number of lit lights {lights.number_lit}')


if __name__ == '__main__':
    main()
