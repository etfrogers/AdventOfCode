from utils import Point

INSTRUCTIONS = {'<': Point(-1, 0),
                '>': Point(1, 0),
                '^': Point(0, 1),
                'v': Point(0, -1),
                }


def get_number_of_unique_houses(houses):
    return len(set(houses))


def get_visits(instructions: str):
    pos = Point(0, 0)
    visited = [pos.tuple]
    for instruction in instructions:
        pos += INSTRUCTIONS[instruction]
        visited.append(pos.tuple)
    return visited


def main():
    with open('input.txt') as f:
        instructions = f.readline()
    houses = get_visits(instructions)
    unique_houses = get_number_of_unique_houses(houses)
    print(f'Part 1: Number of unique houses is {unique_houses}')


if __name__ == '__main__':
    main()
