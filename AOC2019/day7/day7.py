import itertools

from AOC2019.day5.day5 import IntCodeComputer2


def optimise_phases(instructions):
    best_thrust = 0
    best_phases = None
    for phases in itertools.permutations(range(5)):
        starting_thrust = 0
        for phase in phases:
            comp = IntCodeComputer2(instructions, [phase, starting_thrust])
            comp.execute()
            assert len(comp.output_data) == 1
            starting_thrust = comp.output_data[0]
        if starting_thrust > best_thrust:
            best_thrust = starting_thrust
            best_phases = tuple(phases)
    return best_thrust, best_phases


def main():
    with open('input.txt') as f:
        instructions = f.readline()

    thrust, phases = optimise_phases(instructions)

    print(f'Optimal thrust: {thrust} - {phases}')


if __name__ == '__main__':
    main()
