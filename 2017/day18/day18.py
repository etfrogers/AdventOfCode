from collections import defaultdict


class SoundCard:

    def __init__(self, instruction_list):
        self.last_played = None
        self.registers = defaultdict(lambda: 0)
        do_nothing = lambda x: x
        self.instruction_dict = {'snd': {'func': self.sound, 'conv': chr},
                                 'set': {'func': self.set, 'conv': [chr, int]},
                                 'add': {'func': self.add, 'conv': [chr, int]},
                                 'mul': {'func': self.multiply, 'conv': [chr, int]},
                                 'mod': {'func': self.modulo, 'conv': [chr, int]},
                                 'rcv': {'func': self.recover, 'conv': chr},
                                 'jgz': {'func': self.jump, 'conv': chr},
                                 }
        self.instructions = [self.parse_instruction(i) for i in instruction_list]
        self.finished = False
        self.pointer = 0

    def execute(self):
        self.finished = False
        self.pointer = 0
        while not self.finished:
            instruction = self.instructions[self.pointer]

            self.pointer += 1  # if not jumped?

    def sound(self, register):
        self.last_played = self.registers[register]

    def set(self, register, value):
        self.registers[register] = value

    def add(self, register, value):
        self.registers[register] += value

    def multiply(self, register, value):
        self.registers[register] *= value

    def modulo(self, register, value):
        self.registers[register] %= value

    def recover(self, register):
        if self.registers[register] != 0:
            print('Recovered value: %d' % self.last_played)
            self.finished = True

    def jump(self, register, value):
        if self.registers[register] != 0:
            self.pointer += value

    def parse_instruction(self, instruction_text):
        tokens = instruction_text.split()
        d = self.instruction_dict[tokens[0]]
        convert = d['conv']
        if len(tokens) > 2:
            args = (f(*v) for f, v in zip(convert, tokens[1:]))
        else:
            args = convert(tokens[1])
        instruction = {'func': d['func'],
                       'args': args}
        return instruction


def main():
    with open('test_input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    print(instructions)
    snd = SoundCard(instructions)
    snd.execute()


if __name__ == '__main__':
    main()
