import math
import re


def parse_fight_spec(spec):
    army1_spec, army2_spec = spec.split('\n\n')

    army1 = Army(army1_spec)
    army2 = Army(army2_spec)
    return army1, army2


def join_indented_lines(lst):
    output = []
    for item in lst:
        if item[0] == ' ':
            output[-1] += item
        else:
            output.append(item)
    return output


class Fight:
    def __init__(self, spec):
        self._initial_spec = spec
        self.armies = {}
        self.create_from_spec(spec)

    def reset(self):
        self.create_from_spec(self._initial_spec)

    def create_from_spec(self, spec):
        self.armies = {army.name: army for army in parse_fight_spec(spec)}

    def get_army(self, name):
        return self.armies[name]

    def __getitem__(self, item):
        return self.armies[item]

    def target_selection(self):
        return {id_: army.select_targets(army.get_other_army(self.armies)) for id_, army in self.armies.items()}

    def do_attacks(self, targets):
        all_units = [(army.name, id_, unit) for army in self.armies.values() for id_, unit in army.groups.items()]
        all_units.sort(reverse=True, key=lambda u: u[2].initiative)
        result = []
        for army_name, attack_id, attacker in all_units:
            attack_army = self[army_name]
            defend_army = attack_army.get_other_army(self.armies)
            defender_id = targets[army_name][attack_id]
            if defender_id is None:
                continue
            defender = defend_army[defender_id]
            starting_units = defender.units
            try:
                killed_units = attacker.attack(defender)
            except UnitDied:
                defend_army.groups.pop(defender_id)
                killed_units = starting_units
            result.append((army_name, attack_id, defender_id, killed_units))
        return result

    def do_round(self):
        targets = self.target_selection()
        result = self.do_attacks(targets)
        _, _, _, killed_units = zip(*result)
        if all([k == 0 for k in killed_units]):
            raise DeadlockException
        return result

    def run(self):
        while all(army.groups for army in self.armies.values()):
            self.do_round()

    def outcome(self):
        return sum([g.units for g in self.get_winner().groups.values()])

    def get_winner(self):
        return [army for army in self.armies.values() if army.groups][0]

    def run_with_boost(self, boost):
        self.reset()
        self.apply_boost(boost)
        self.run()

    def find_min_boost(self):
        low_boost = 1
        high_boost = math.inf
        while high_boost - low_boost > 1:
            if high_boost == math.inf:
                test_boost = low_boost * 10
            else:
                test_boost = (low_boost + high_boost) // 2
            print(f'Trying boost: {test_boost}')
            try:
                self.run_with_boost(test_boost)
                winner_name = self.get_winner().name
            except DeadlockException:
                winner_name = 'Infection'  # if a deadlock then immune system didn't win, which is what we search for
            if winner_name == 'Immune System':
                assert test_boost < high_boost
                high_boost = test_boost
            if winner_name == 'Infection':
                assert test_boost > low_boost
                low_boost = test_boost
        return high_boost

    def apply_boost(self, boost):
        for group in self['Immune System'].groups.values():
            group.attack_damage += boost


class Army:
    def __init__(self, spec):
        name, *spec = spec.split('\n')
        assert name[-1] == ':'
        name = name[0:-1]
        spec = join_indented_lines(spec)
        self.name = name
        self.groups = {i+1: Group(line) for i, line in enumerate(spec)}

    def __getitem__(self, item):
        return self.groups[item]

    def select_targets(self, other):
        group_list = list(self.groups.items())
        group_list.sort(reverse=True, key=lambda g: (g[1].effective_power, g[1].initiative))
        targeted = set()
        targets = {}
        for attacker_id, group in group_list:
            lst = [(group.damage_dealt_to(target), target.effective_power, target.initiative, id_)
                   for id_, target in other.groups.items() if id_ not in targeted]
            lst.sort(reverse=True)
            if lst and lst[0][0] > 0:
                defender_id = lst[0][3]
                targets[attacker_id] = defender_id
                targeted.add(defender_id)
            else:
                targets[attacker_id] = None
        return targets

    def get_other_army(self, armies):
        return [a for a in armies.values() if a is not self][0]


class Group:
    PATTERN = re.compile(r'(\d+) units each with (\d+) hit points (\((immune to ([a-z, ]+))?(; )?(weak to ([a-z, ]+))?\) )?' +
                         r'with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)')

    def __init__(self, spec):
        matches = self.PATTERN.match(spec)
        units, hit_points, _, _, immunities, _, _, weaknesses, attack_damage, attack_type, initiative = matches.groups()
        self._units = int(units)
        self.hit_points = int(hit_points)
        self.attack_damage = int(attack_damage)
        self.attack_type = attack_type
        self.initiative = int(initiative)
        self.weaknesses = set('') if weaknesses is None else set(weaknesses.split(', '))
        self.immunities = set('') if immunities is None else set(immunities.split(', '))

    @property
    def effective_power(self):
        return self.units * self.attack_damage

    def damage_dealt_to(self, other):
        modifier = 1
        if self.attack_type in other.immunities:
            modifier = 0
        elif self.attack_type in other.weaknesses:
            modifier = 2
        return self.effective_power * modifier

    def attack(self, other):
        damage = self.damage_dealt_to(other)
        lost_units = other.take_damage(damage)
        return lost_units

    def take_damage(self, damage):
        lost_units = damage // self.hit_points
        self.units -= lost_units
        return lost_units

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self._units = value
        if self._units <= 0:
            self._units = 0
            raise UnitDied


class UnitDied(Exception):
    pass


class DeadlockException(Exception):
    pass


def main():
    with open('input.txt') as f:
        specs = f.read()
    fight = Fight(specs)
    fight.run()

    print('Part 1: ', fight.outcome())

    min_boost = fight.find_min_boost()
    fight.run_with_boost(min_boost)
    print(f'Part 2:\nMin boost: {min_boost}\nRemaining Units {fight.outcome()}')


if __name__ == '__main__':
    main()
