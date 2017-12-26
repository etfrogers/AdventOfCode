import day16


def test_1():
    with open('test_input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = dance_moves.split(',')
    dancers = day16.Dancers(5)

    dancers.perform(dance_moves)
    assert dancers.formation == 'baedc'


def test_part1():
    with open('input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = dance_moves.split(',')
    dancers = day16.Dancers(16)

    dancers.perform(dance_moves)
    assert dancers.formation == 'kgdchlfniambejop'

