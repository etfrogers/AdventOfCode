import day18


def test_rcv1():
    with open('test_input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    snd = day18.SoundCard(instructions)
    assert snd.execute() == 4


def test_part1():
    with open('input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    snd = day18.SoundCard(instructions)
    assert snd.execute() == 4601


def test_part2a():
    with open('test_input2.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    prog0 = day18.Program(instructions, 0)
    prog1 = day18.Program(instructions, 1)
    cluster = day18.Cluster([prog0, prog1])
    cluster.execute()
    assert prog1.send_counter == 3


def test_part2():
    with open('input.txt', 'r') as file:
        instructions = file.readlines()
    instructions = [line.strip() for line in instructions]
    prog0 = day18.Program(instructions, 0)
    prog1 = day18.Program(instructions, 1)
    cluster = day18.Cluster([prog0, prog1])
    cluster.execute()
    assert prog1.send_counter == 6858