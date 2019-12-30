import itertools

from AOC2019.day5.day5 import IntCodeComputer2


class AsyncIntCodeComputer(IntCodeComputer2):
    def __init__(self, instructions, input_=None):
        super().__init__(instructions, input_)
        self.paused = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
        self.execute()

    def input(self, modes):
        if len(self.input_data) == 0:
            self.pause()
            return
        super().input(modes)

    def execute(self):
        while not (self.finished or self.paused):
            opcode_, modes = self.get_opcode()
            opcode_(modes)


def optimise_phases(instructions, use_feedback=False):
    best_thrust = 0
    best_phases = None
    if use_feedback:
        possible_phases = range(5, 10)
    else:
        possible_phases = range(5)
    for phases in itertools.permutations(possible_phases):
        current_thrust = 0
        if use_feedback:
            current_thrust = run_feedback_amplifiers(instructions, phases)
        else:
            for phase in phases:
                comp = IntCodeComputer2(instructions, [phase, current_thrust])
                comp.execute()
                assert len(comp.output_data) == 1
                current_thrust = comp.output_data[0]
        if current_thrust > best_thrust:
            best_thrust = current_thrust
            best_phases = tuple(phases)
    return best_thrust, best_phases


def run_feedback_amplifiers(instructions, phases):
    amps = [AsyncIntCodeComputer(instructions, [phase]) for phase in phases]
    current_thrust = 0
    while not all([amp.finished for amp in amps]):
        for amp in amps:
            amp.input_data.push(current_thrust)
            amp.resume()
            current_thrust = amp.output_data.pop()
    return current_thrust


def main():
    with open('input.txt') as f:
        instructions = f.readline()

    thrust, phases = optimise_phases(instructions)
    print(f'Optimal thrust: {thrust} - {phases}')

    thrust, phases = optimise_phases(instructions, use_feedback=True)
    print(f'Optimal thrust with feedback: {thrust} - {phases}')


if __name__ == '__main__':
    main()
