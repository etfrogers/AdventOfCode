from collections import defaultdict


class AssemblyInterpreter:
    def __init__(self, instruction_list):
        # self.instruction_dict must be set before this constructor is called.
        try:
            self.__dict__['instruction_dict']
        except KeyError:
            raise AttributeError('self.instruction_dict must be set before this constructor is called.')
        self.registers = defaultdict(lambda: 0)
        self.instructions = [self.parse_instruction(i) for i in instruction_list]
        self.finished = False
        self.pointer = 0

    def execute(self, show_status=False):
        self.finished = False
        retval = None
        if show_status:
            print(self.register_string)
        while retval is None and self.pointer < len(self.instructions):

            instruction = self.instructions[self.pointer]
            if show_status:
                print(instruction_to_string(instruction))
            retval = instruction['func'](*instruction['args'])
            self.pointer += 1

            if show_status:
                print(self.register_string)
        return retval

    def get_value(self, value):
        try:
            val = int(value)
        except ValueError:
            val = self.registers[value]
        return val

    def parse_instruction(self, instruction_text):
        tokens = instruction_text.split()
        # print(tokens)
        args = tuple(tokens[1:])
        instruction = {'func': self.instruction_dict[tokens[0]], 'args': args}
        return instruction

    @property
    def register_string(self):
        labels = []
        values = []
        for entry in sorted(self.registers.items()):
            labels.append('{:>3}'.format(entry[0]))
            values.append('{:>3}'.format(entry[1]))
        return ' '.join(labels) + '\n' + ' '.join(values)


def instruction_to_string(instruction):
    return instruction['func'].__name__ + '(' + str(instruction['args']) + ')'
