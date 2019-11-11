from AOC2015.day21.day21 import Character, load_kit_list, BOSS_PATTERN, optimise_gold_for_result


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


def test_part1():
    kit_list = load_kit_list()
    with open('input.txt') as file:
        boss_spec = file.read()
    match = BOSS_PATTERN.match(boss_spec)
    player = Character(100, 0, 0)
    boss = Character(*(int(v) for v in match.groups()))
    winning_cost = optimise_gold_for_result(kit_list, player, boss)
    assert winning_cost == 121


def test_part2():
    kit_list = load_kit_list()
    with open('input.txt') as file:
        boss_spec = file.read()
    match = BOSS_PATTERN.match(boss_spec)
    player = Character(100, 0, 0)
    boss = Character(*(int(v) for v in match.groups()))
    losing_cost = optimise_gold_for_result(kit_list, player, boss, min_to_lose=True)
    assert losing_cost == 201
