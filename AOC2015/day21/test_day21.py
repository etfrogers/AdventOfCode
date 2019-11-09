from AOC2015.day21.day21 import Character


def test_damage_on():
    player = Character(8, 5, 5)
    boss = Character(12, 7, 2)
    assert player.calc_damage_on(boss) == 3
    assert boss.calc_damage_on(player) == 2


def test_fight():
    player = Character(8, 5, 5)
    boss = Character(12, 7, 2)
    winner = Character.fight(player, boss)
    assert winner is player
    assert player.hit_points == 2
