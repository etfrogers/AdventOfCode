import re
from collections import defaultdict


class Bot:
    def __init__(self):
        self.high = None
        self.low = None
        self._inputs = [None, None]

    def set_input(self, value):
        first_none = self._inputs.index(None)
        self._inputs[first_none] = value
        if not any([v is None for v in self._inputs]):
            self.high.set_input(self.high_val)
            self.low.set_input(self.low_val)

    @property
    def low_val(self):
        return min(self._inputs)

    @property
    def high_val(self):
        return max(self._inputs)

    @property
    def inputs(self):
        return sorted(self._inputs)

    def compares(self, pair):
        return all([a == b for a, b in zip(self.inputs, sorted(pair))])

    def __str__(self):
        return 'L: [{}]  -> , H: [{}] -> '.format(self.low_val, self.high_val)


class Output(Bot):
    def __init__(self):
        super().__init__()
        self._inputs = [None]  # Force length to 1

    def set_input(self, value):
        first_none = self._inputs.index(None)  # complex setting to mirror case in Bot
        self._inputs[first_none] = value

    def __str__(self):
        return '[{}]'.format(self._inputs[0])


class Factory:
    def __init__(self, instructions):
        self.bots = defaultdict(lambda: Bot())
        self.inputs = {}
        self.outputs = defaultdict(lambda: Output())
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
            self.inputs[value] = bot
        else:
            match = self.bot_rule_exp.match(instruction)
            if not match:
                raise ValueError
            giver_id = int(match[1])
            low_type = match[2]
            low_id = int(match[3])
            high_type = match[4]
            high_id = int(match[5])
            low_dest = self.bots[low_id] if low_type == 'bot' else self.outputs[low_id]
            self.bots[giver_id].low = low_dest
            high_dest = self.bots[high_id] if high_type == 'bot' else self.outputs[high_id]
            self.bots[giver_id].high = high_dest

    def fill_values(self):
        for val, dest in self.inputs.items():
            dest.set_input(val)

    def __str__(self):
        lst = [
                '\n'.join([str(id) + ': ' + str(bot) for id, bot in self.bots.items()]),
                '\t'.join(['{} -> {}'.format(output, id) for id, output in self.outputs.items()])
              ]
        return '\n'.join(lst)

    def get_comparator(self, pair):
        return [(id, bot) for id, bot in self.bots.items() if bot.compares(pair)]


def main():
    with open('day10_input.txt') as file:
        instructions = file.readlines()
    instructions = [i.strip() for i in instructions]
    print(instructions)
    factory = Factory(instructions)
    print(str(factory))
    print(factory.get_comparator((17, 61)))


if __name__ == '__main__':
    main()
