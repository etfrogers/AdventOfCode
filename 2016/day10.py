import re
from collections import defaultdict

class Link:
    def __init__(self, source=None, dest=None, value=None):
        self.source = source
        self.dest = dest
        self.value = value

    def isempty(self):
        return self.dest is None


class Bot:
    def __init__(self):
        self.high = Link()
        self.low = Link()
        self.in1 = Link()
        self.in2 = Link()

    @property
    def next_input(self):
        if self.in1.isempty():
            return self.in1
        elif self.in2.isempty():
            return self.in2
        else:
            raise ValueError

    @next_input.setter
    def next_input(self, value):
        if self.in1.isempty():
            self.in1 = value
        elif self.in2.isempty():
            self.in2 = value
        else:
            raise ValueError


class Factory:
    def __init__(self, instructions):
        self.bots = defaultdict(lambda: Bot())
        self.inputs = []
        self.outputs = []
        self.instructions = instructions
        self.parse_instructions()
        self.fill_values()

    def parse_instructions(self):
        for inst in self.instructions:
            self.parse_instruction(inst)

    value_exp = re.compile(r'value (\d+) goes to bot (\d+)')
    bot_rule_exp = re.compile(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)')

    def parse_instruction(self, instruction):
        match = self.value_exp.match(instruction)
        if match:
            bot_id = int(match[2])
            value = int(match[1])
            bot = self.bots[bot_id]
            self.inputs.append(Link(source='input', dest=bot, value=value))
        else:
            match = self.bot_rule_exp.match(instruction)
            if not match:
                raise ValueError
            giver_id = int(match[1])
            low_type = match[2]
            low_id = int(match[3])
            high_type = match[4]
            high_id = int(match[5])
            low_dest = self.bots[low_id] if low_type == 'bot' else 'output {}'.format(low_id)
            self.bots[giver_id].low = Link(low_dest)
            high_dest = self.bots[high_id] if high_type == 'bot' else 'output {}'.format(high_id)
            self.bots[giver_id].high = Link(high_dest)

    def fill_values(self):
        for input in self.inputs:
            input.dest.next_input = input


def main():
    with open('day10_test_input.txt') as file:
        instructions = file.readlines()
    instructions = [i.strip() for i in instructions]
    print(instructions)
    factory = Factory(instructions)
    print(factory)


if __name__ == '__main__':
    main()