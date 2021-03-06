from AOC2015.day14.day14 import Reindeer, State

test_input = '''Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.'''


def test_1():
    specs = test_input.split('\n')
    reindeer = [Reindeer(s) for s in specs]
    Reindeer.race(reindeer, 1000)
    assert all([r.state == State.RESTING for r in reindeer])
    assert reindeer[0].name == 'Comet'
    assert reindeer[0].position == 1120
    assert reindeer[1].name == 'Dancer'
    assert reindeer[1].position == 1056


def test_2():
    specs = test_input.split('\n')
    reindeer = [Reindeer(s) for s in specs]
    Reindeer.race(reindeer, 1000)
    assert reindeer[0].name == 'Comet'
    assert reindeer[0].points == 312
    assert reindeer[1].name == 'Dancer'
    assert reindeer[1].points == 689


def test_part_1():
    with open('input.txt') as f:
        specs = f.readlines()
    reindeer = [Reindeer(s) for s in specs]
    Reindeer.race(reindeer, 2503)
    winners = Reindeer.get_winner(reindeer)
    assert len(winners) == 1, 'We have a draw!'
    winner = winners[0]
    assert winner.name == 'Donner'
    assert winner.position == 2655


def test_part_2():
    with open('input.txt') as f:
        specs = f.readlines()
    reindeer = [Reindeer(s) for s in specs]
    Reindeer.race(reindeer, 2503)
    winners = Reindeer.get_winner(reindeer, on_points=True)
    assert len(winners) == 1, 'We have a draw!'
    winner = winners[0]
    assert winner.name == 'Vixen'
    assert winner.points == 1059
