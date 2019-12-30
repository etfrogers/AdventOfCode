from AOC2019.day9.day9 import RelativeIntCodeComputer


class IntCodeComputer(RelativeIntCodeComputer):
    def __init__(self, instructions, input_=None):
        try:
            with open(instructions) as file:
                instructions = file.read().strip()
        except FileNotFoundError:
            pass
        super().__init__(instructions, input_)