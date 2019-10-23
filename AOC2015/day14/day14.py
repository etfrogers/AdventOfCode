import re
from enum import Enum


class State(Enum):
    RUNNING = 0
    RESTING = 1


class Reindeer:
    PATTERN = re.compile(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.')

    def __init__(self, spec):
        matches = self.PATTERN.match(spec)
        self.name = matches.group(1)
        self.speed = int(matches.group(2))
        self.run_time = int(matches.group(3))
        self.rest_time = int(matches.group(4))
        self.position = 0
        self.been_running = 0
        self.been_resting = 0
        self.state = None
        self.points = 0
        self.start_running()

    def start_running(self):
        self.state = State.RUNNING
        self.been_running = 0

    def start_resting(self):
        self.state = State.RESTING
        self.been_resting = 0

    def step(self):
        if self.state == State.RUNNING:
            self.been_running += 1
            self.position += self.speed
            if self.been_running >= self.run_time:
                self.start_resting()
        elif self.state == State.RESTING:
            self.been_resting += 1
            if self.been_resting >= self.rest_time:
                self.start_running()

    @staticmethod
    def race(reindeer, time):
        for _ in range(time):
            for r in reindeer:
                r.step()
            for r in Reindeer.get_winner(reindeer):
                r.points += 1

    @staticmethod
    def get_winner(reindeer, on_points=False):
        if not on_points:
            max_distance = max([r.position for r in reindeer])
            winners = [r for r in reindeer if r.position == max_distance]
        else:
            max_points = max([r.points for r in reindeer])
            winners = [r for r in reindeer if r.points == max_points]
        return winners


def main():
    with open('input.txt') as f:
        specs = f.readlines()
    reindeer = [Reindeer(s) for s in specs]
    Reindeer.race(reindeer, 2503)
    winners = Reindeer.get_winner(reindeer)
    assert len(winners) == 1, 'We have a draw!'
    winner = winners[0]
    print(f'Part 1: Winner is {winner.name} with a distance of {winner.position}')

    winners = Reindeer.get_winner(reindeer, on_points=True)
    assert len(winners) == 1, 'We have a draw!'
    winner = winners[0]
    print(f'Part 2: Winner is {winner.name} with {winner.points} points')


if __name__ == '__main__':
    main()
