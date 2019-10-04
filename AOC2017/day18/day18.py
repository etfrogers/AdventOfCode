from collections import deque
from assembly_interpreter import AssemblyInterpreter


class SoundCard(AssemblyInterpreter):

    def __init__(self, instruction_list):
        self.last_played = None
        self.instruction_dict = {'snd': self.snd,
                                 'set': self.set,
                                 'add': self.add,
                                 'mul': self.multiply,
                                 'mod': self.modulo,
                                 'rcv': self.rcv,
                                 'jgz': self.jump,
                                 }
        super().__init__(instruction_list)

    def snd(self, value):
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

    def rcv(self, register):
        if self.registers[register] != 0:
            print('Recovered value: %d' % self.last_played)
            return self.last_played

    def jump(self, register, value):
        if self.get_value(register) > 0:
            self.pointer += self.get_value(value) - 1


class Program(SoundCard):
    def __init__(self, instruction_list, prog_id):
        super().__init__(instruction_list)
        self.prog_id = prog_id
        self.queue = deque([])
        self.send_counter = 0
        self.registers['p'] = prog_id
        self.cluster = None

    def snd(self, value):  # send
        val = self.get_value(value)
        id_to_send_to = 1 if self.prog_id == 0 else 0
        prog_to_send_to = self.cluster.get_prog(id_to_send_to)
        prog_to_send_to.queue.append(val)
        self.send_counter += 1

    def rcv(self, register):  # receive
        if self.queue:
            self.registers[register] = self.queue.popleft()
        else:
            self.pointer -= 1  # prevent pointer increment, as instruction halted before execution
            return True  # returning anything other than None breaks out of execute loop


class Cluster:
    def __init__(self, prog_list):
        self.prog_list = prog_list
        for p in prog_list:
            p.cluster = self

    def get_prog(self, prog_id):
        for p in self.prog_list:
            if p.prog_id == prog_id:
                return p
        return None

    def execute(self):
        deadlocked = False
        while not deadlocked:
            for p in self.prog_list:
                p.execute()
            deadlocked = all([not p.queue for p in self.prog_list])


def main():
    with open('input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    print(instructions)
    prog0 = Program(instructions, 0)
    prog1 = Program(instructions, 1)
    cluster = Cluster([prog0, prog1])
    cluster.execute()
    print(prog1.send_counter)


if __name__ == '__main__':
    main()
