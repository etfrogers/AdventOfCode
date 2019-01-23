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
        self.army1, self.army2 = parse_fight_spec(spec)


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


class Group:
    PATTERN = re.compile(r'(\d+) units each with (\d+) hit points (\((immune to ([a-z, ]+); )?weak to ([a-z, ]+)\))? ' +
                         r'with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)')

    def __init__(self, spec):
        matches = self.PATTERN.match(spec)
        units, hit_points, _, _, immunities, weaknesses, attack_damage, attack_type, initiative = matches.groups()
        print(matches.groups())
        self.units = int(units)
        self.hit_points = int(hit_points)
        self.attack_damage = int(attack_damage)
        self.attack_type = attack_type
        self.initiative = int(initiative)
        self.weaknesses = set('') if weaknesses is None else set(weaknesses.split(', '))
        self.immunities = set('') if immunities is None else set(immunities.split(', '))
