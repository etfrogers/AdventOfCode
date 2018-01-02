from collections import defaultdict


class SoundCard:

    def __init__(self, instruction_list):
        self.last_played = None
        self.registers = defaultdict(lambda: 0)
        self.instruction_dict = {'snd': self.sound,
                                 'set': self.set,
                                 'add': self.add,
                                 'mul': self.multiply,
                                 'mod': self.modulo,
                                 'rcv': self.recover,
                                 'jgz': self.jump,
                                 }
        self.instructions = [self.parse_instruction(i) for i in instruction_list]
        self.finished = False
        self.pointer = 0
        self.jumped = False

    def execute(self):
        self.finished = False
        self.pointer = 0
        while not self.finished:
            instruction = self.instructions[self.pointer]
            instruction['func'](*instruction['args'])
            if not self.jumped:
                self.pointer += 1  # if not jumped?
                self.jumped = False

    def get_value(self, value):
        try:
            val = int(value)
        except ValueError:
            val = self.registers[value]
        return val

    def sound(self, value):
        val = self.get_value(value)
        self.last_played = val
        print('Playing: %d' % val)

    def set(self, register, value):
        self.registers[register] = self.get_value(value)

    def add(self, register, value):
        self.registers[register] += self.get_value(value)

    def multiply(self, register, value):
        self.registers[register] *= self.get_value(value)

    def modulo(self, register, value):
        self.registers[register] %= self.get_value(value)

    def recover(self, register):
        if self.registers[register] != 0:
            print('Recovered value: %d' % self.last_played)
            self.finished = True
            return self.last_played

    def jump(self, register, value):
        if self.registers[register] != 0:
            self.pointer += self.get_value(value)
            self.jumped = True

    def parse_instruction(self, instruction_text):
        tokens = instruction_text.split()
        print(tokens)
        args = tuple(tokens[1:])
        instruction = {'func': self.instruction_dict[tokens[0]], 'args': args}
        return instruction


def main():
    with open('test_input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    print(instructions)
    snd = SoundCard(instructions)
    print(snd.execute())


if __name__ == '__main__':
    main()
