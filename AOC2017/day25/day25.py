import collections
import re


class TuringMachine:
    header_exp = re.compile('''Begin in state ([A-Z]).
Perform a diagnostic checksum after ([0-9]+) steps.''')

    state_exp = re.compile('''In state ([A-Z]):
  If the current value is 0:
    - Write the value ([01]).
    - Move one slot to the (right|left).
    - Continue with state ([A-Z]).
  If the current value is 1:
    - Write the value ([01]).
    - Move one slot to the (right|left).
    - Continue with state ([A-Z]).''')

    dir_to_pos = {'right': 1, 'left': -1}

    def __init__(self, blueprints):
        parts = blueprints.split('\n\n')
        headers = parts[0]
        state_blueprints = parts[1:]
        self.current_state, self.run_length = self.parse_headers(headers)
        self.tape = collections.defaultdict(int)
        self.states = self.parse_states(state_blueprints)
        self.cursor = 0

    @staticmethod
    def parse_states(state_blueprints):
        states = {}
        for blueprint in state_blueprints:
            m = TuringMachine.state_exp.match(blueprint)
            name = m.group(1)
            new_val_0 = int(m.group(2))
            dir_0 = TuringMachine.dir_to_pos[m.group(3)]
            new_state_0 = m.group(4)
            new_val_1 = int(m.group(5))
            dir_1 = TuringMachine.dir_to_pos[m.group(6)]
            new_state_1 = m.group(7)
            states[name] = {0: {'new val': new_val_0, 'new state': new_state_0, 'dir': dir_0},
                            1: {'new val': new_val_1, 'new state': new_state_1, 'dir': dir_1}}
        return states

    def run(self):
        steps = 0
        #self.print()
        while steps < self.run_length:
            curr_val = self.tape[self.cursor]
            ops = self.states[self.current_state][curr_val]
            self.tape[self.cursor] = ops['new val']
            self.current_state = ops['new state']
            self.cursor += ops['dir']
            steps += 1
        #    self.print()

    def print(self):
        output = ['...']
        min_val = -3  # min(self.tape.keys())
        max_val = 2  # max(self.tape.keys())
        for i in range(min_val, max_val+1):
            output.append(' '
                          + ('[' if i == self.cursor else ' ')
                          + str(self.tape[i])
                          + (']' if i == self.cursor else ' ')
                          + ' ')
        output.append('...')
        output.append(' Will run ' + self.current_state)
        print(''.join(output))

    def get_checksum(self):
        return sum(self.tape.values())

    @staticmethod
    def parse_headers(headers):
        m = TuringMachine.header_exp.match(headers)
        initial_state = m.group(1)
        run_length = int(m.group(2))
        return initial_state, run_length


def main():
    with open('input.txt', 'r') as file:
        blueprints = file.read()
    tm = TuringMachine(blueprints)
    tm.run()
    print(tm.get_checksum())


if __name__ == '__main__':
    main()
