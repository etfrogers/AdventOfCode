from collections import deque


class Player:
    def __init__(self, id):
        self.id = id
        self.score = 0


SPECIAL_MARBLE = 23


def play_marbles(n_players, last_marble):
    players = [Player(id+1) for id in range(n_players)]

    marbles = deque([0])

    for marble_number in range(1, last_marble+1):
        player = players[(marble_number-1) % n_players]
        if marble_number % SPECIAL_MARBLE == 0:
            player.score += marble_number
            marbles.rotate(-7)
            player.score += marbles.pop()
        else:
            marbles.rotate(2)
            marbles.append(marble_number)
    high_score = max([p.score for p in players])
    return high_score


if __name__ == '__main__':
    print(play_marbles(477, 70851))

    print(play_marbles(477, 7085100))