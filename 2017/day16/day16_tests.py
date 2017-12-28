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


def test_fast_whole_dance1():
    with open('input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = dance_moves.split(',')
    dancers = day16.Dancers(16)

    reps = 50
    dancers.whole_dance(dance_moves, reps, day16.Speed.SLOW)
    slow_formation = dancers.formation
    dancers.whole_dance(dance_moves, reps, day16.Speed.FAST)
    faster_formation = dancers.formation

    assert slow_formation == faster_formation


def test_fast_whole_dance2():
    with open('test_input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = dance_moves.split(',')
    dancers = day16.Dancers(5)

    reps = 100
    dancers.whole_dance(dance_moves, reps, day16.Speed.SLOW)
    slow_formation = dancers.formation
    dancers.whole_dance(dance_moves, reps, day16.Speed.FAST)
    faster_formation = dancers.formation

    assert slow_formation == faster_formation


def test_part2():
    reps = int(1e9)
    with open('input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = dance_moves.split(',')
    dancers = day16.Dancers(16)

    dancers.whole_dance(dance_moves, reps, day16.Speed.FAST)
    assert dancers.formation == 'fjpmholcibdgeakn'
