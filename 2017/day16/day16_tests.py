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


def test_reposition():
    with open('input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = dance_moves.split(',')
    dancers = day16.Dancers(16)

    dancers.perform(dance_moves)
    first_formation = dancers.formation
    dancers.store_reposition()
    dancers.reset()
    dancers.apply_reposition()
    second_formation = dancers.formation

    assert first_formation == second_formation


def test_reposition2():
    with open('input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = dance_moves.split(',')
    dancers = day16.Dancers(16)

    dancers.perform(dance_moves)
    dancers.store_reposition()
    dancers.perform(dance_moves)
    first_formation = dancers.formation
    dancers.reset()
    dancers.apply_reposition()
    dancers.apply_reposition()
    second_formation = dancers.formation

    assert first_formation == second_formation


def test_reposition3():
    with open('test_input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = dance_moves.split(',')
    dancers = day16.Dancers(5)

    dancers.perform(dance_moves)
    dancers.store_reposition()
    first_formation = dancers.formation
    dancers.reset()
    dancers.apply_reposition()
    second_formation = dancers.formation

    assert first_formation == second_formation


def test_reposition4():
    with open('test_input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = 's1,x3/4,s3,x1/4,x3/1,s4,pa/dx4/1'
    dance_moves = dance_moves.split(',')
    dancers = day16.Dancers(5)

    print(dancers.formation)
    dancers.perform(dance_moves)
    print(dancers.formation)
    dancers.store_reposition()
    dancers.perform(dance_moves)
    print(dancers.formation)
    first_formation = dancers.formation
    dancers.reset()
    dancers.apply_reposition()
    dancers.apply_reposition()
    second_formation = dancers.formation

    assert first_formation == second_formation


def test_fast_whole_dance1():
    with open('input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = dance_moves.split(',')
    dancers = day16.Dancers(16)

    reps = 10
    dancers.whole_dance(dance_moves, reps, day16.Speed.SLOW)
    slow_formation = dancers.formation
    dancers.whole_dance(dance_moves, reps, day16.Speed.FASTER)
    faster_formation = dancers.formation

    assert slow_formation == faster_formation


def test_faster_whole_dance1():
    with open('input.txt', 'r') as file:
        dance_moves = file.read()
    dance_moves = dance_moves.strip()
    dance_moves = dance_moves.split(',')
    dancers = day16.Dancers(16)

    reps = 200
    dancers.whole_dance(dance_moves, reps, day16.Speed.FASTER)
    slow_formation = dancers.formation

    dancers.whole_dance(dance_moves, reps, day16.Speed.FASTEST)
    faster_formation = dancers.formation

    assert slow_formation == faster_formation
