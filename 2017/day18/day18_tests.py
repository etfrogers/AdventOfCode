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
