import re

from AOC2018.day24 import day24

test_input = '''Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with
 an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning,
 slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack
 that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire,
 cold) with an attack that does 12 slashing damage at initiative 4'''


DAMAGE_PATTERN = re.compile(r'([A-za-z ]+) group (\d+) would deal defending group (\d+) (\d+) damage')
RESULT_PATTERN = re.compile(r'([A-za-z ]+) group (\d+) attacks defending group (\d+), killing (\d+) units')


def test_parsing():
    fight = day24.Fight(test_input)
    assert len(fight['Immune System'].groups) == 2
    assert len(fight['Infection'].groups) == 2
    assert fight['Immune System'][1].attack_damage == 4507
    assert fight['Immune System'][2].units == 989
    assert 'radiation' in fight['Infection'][2].immunities
    assert fight['Infection'][1].initiative == 1


def test_fighting():
    fight = day24.Fight(test_input)
    outputs = test_output.split('\n\n\n')
    _, damage_spec, round_spec = outputs[0].split('\n\n')
    yield check_damage, fight, damage_spec
    yield check_round, fight, round_spec


def check_round(fight, round_spec):
    results = fight.do_round()
    for result, line in zip(results, round_spec.split('\n')):
        matches = RESULT_PATTERN.match(line)
        assert matches.groups() == tuple(str(i) for i in result)


def check_damage(fight: day24.Fight, spec):
    for line in spec.split('\n'):
        matches = DAMAGE_PATTERN.match(line)
        army, attack_group, defend_group, damage = matches.groups()
        attack_group = int(attack_group)
        defend_group = int(defend_group)
        damage = int(damage)
        other_army = fight[army].get_other_army(fight.armies).name
        assert fight[army][attack_group].damage_dealt_to(fight[other_army][defend_group]) == damage


def test_outcome():
    fight = day24.Fight(test_input)
    fight.run()
    assert fight.outcome() == 5216


def test_part1():
    with open('input.txt') as f:
        specs = f.read()
    fight = day24.Fight(specs)
    fight.run()

    assert fight.outcome() == 33551


def test_boost():
    fight = day24.Fight(test_input)
    fight.apply_boost(1570)
    fight.run()
    assert fight.get_winner().name == 'Immune System'
    assert fight.outcome() == 51


def test_min_boost():
    fight = day24.Fight(test_input)
    boost = fight.find_min_boost()
    assert boost == 1570
    fight.run_with_boost(boost)
    assert fight.outcome() == 51

# def test_part2():
#     with open('input.txt') as f:
#         specs = f.read()
#     fight = day24.Fight(specs)
#     boost = fight.find_min_boost()
#     assert boost == 33551


test_output = '''Immune System:
Group 1 contains 17 units
Group 2 contains 989 units
Infection:
Group 1 contains 801 units
Group 2 contains 4485 units

Infection group 1 would deal defending group 1 185832 damage
Infection group 1 would deal defending group 2 185832 damage
Infection group 2 would deal defending group 2 107640 damage
Immune System group 1 would deal defending group 1 76619 damage
Immune System group 1 would deal defending group 2 153238 damage
Immune System group 2 would deal defending group 1 24725 damage

Infection group 2 attacks defending group 2, killing 84 units
Immune System group 2 attacks defending group 1, killing 4 units
Immune System group 1 attacks defending group 2, killing 51 units
Infection group 1 attacks defending group 1, killing 17 units


Immune System:
Group 2 contains 905 units
Infection:
Group 1 contains 797 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 184904 damage
Immune System group 2 would deal defending group 1 22625 damage
Immune System group 2 would deal defending group 2 22625 damage

Immune System group 2 attacks defending group 1, killing 4 units
Infection group 1 attacks defending group 2, killing 144 units


Immune System:
Group 2 contains 761 units
Infection:
Group 1 contains 793 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 183976 damage
Immune System group 2 would deal defending group 1 19025 damage
Immune System group 2 would deal defending group 2 19025 damage

Immune System group 2 attacks defending group 1, killing 4 units
Infection group 1 attacks defending group 2, killing 143 units


Immune System:
Group 2 contains 618 units
Infection:
Group 1 contains 789 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 183048 damage
Immune System group 2 would deal defending group 1 15450 damage
Immune System group 2 would deal defending group 2 15450 damage

Immune System group 2 attacks defending group 1, killing 3 units
Infection group 1 attacks defending group 2, killing 143 units


Immune System:
Group 2 contains 475 units
Infection:
Group 1 contains 786 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 182352 damage
Immune System group 2 would deal defending group 1 11875 damage
Immune System group 2 would deal defending group 2 11875 damage

Immune System group 2 attacks defending group 1, killing 2 units
Infection group 1 attacks defending group 2, killing 142 units


Immune System:
Group 2 contains 333 units
Infection:
Group 1 contains 784 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181888 damage
Immune System group 2 would deal defending group 1 8325 damage
Immune System group 2 would deal defending group 2 8325 damage

Immune System group 2 attacks defending group 1, killing 1 unit
Infection group 1 attacks defending group 2, killing 142 units


Immune System:
Group 2 contains 191 units
Infection:
Group 1 contains 783 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181656 damage
Immune System group 2 would deal defending group 1 4775 damage
Immune System group 2 would deal defending group 2 4775 damage

Immune System group 2 attacks defending group 1, killing 1 unit
Infection group 1 attacks defending group 2, killing 142 units


Immune System:
Group 2 contains 49 units
Infection:
Group 1 contains 782 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181424 damage
Immune System group 2 would deal defending group 1 1225 damage
Immune System group 2 would deal defending group 2 1225 damage

Immune System group 2 attacks defending group 1, killing 0 units
Infection group 1 attacks defending group 2, killing 49 units


Immune System:
No groups remain.
Infection:
Group 1 contains 782 units
Group 2 contains 4434 units'''
