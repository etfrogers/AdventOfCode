import re

BOSS_PATTERN = re.compile(r'''Hit Points: (\d+)
Damage: (\d+)
Armor: (\d+)''')


class Character:
    def __init__(self, hit_points, damage, armour):
        self.hit_points = self.base_hit_points = hit_points
        self.base_damage = damage
        self.base_armour = armour
        self.kit = []
        # self.weapon = None
        # self.amour = None
        # self.ring1 = None
        # self.ring2 = None

    def reset(self):
        self.hit_points = self.base_hit_points

    def calc_damage_on(self, other):
        damage = self.damage - other.armour
        if damage < 1:
            damage = 1
        return damage

    def attack(self, other):
        other.hit_points -= self.calc_damage_on(other)

    @property
    def damage(self):
        damage = self.base_damage
        for item in self.kit:
            damage += item.damage
        return damage

    @property
    def armour(self):
        armour = self.base_armour
        for item in self.kit:
            armour += item.armour
        return armour

    @property
    def total_cost(self):
        return sum([i.cost for i in self.kit])

    @staticmethod
    def fight(player, enemy):
        while True:
            player.attack(enemy)
            if enemy.hit_points <= 0:
                return player
            enemy.attack(player)
            if player.hit_points <= 0:
                return enemy


class Item:
    PATTERN = re.compile(r'([a-zA-Z+ \d]+)\s+(\d+)\s+(\d+)\s+(\d+)')

    def __init__(self, category, spec):
        self.category = category
        match = self.PATTERN.match(spec)
        name, cost, damage, armour = match.groups()
        self.name = name.strip()
        self.cost = int(cost)
        self.damage = int(damage)
        self.armour = int(armour)


def load_kit_list():
    with open('kit_list.txt') as file:
        specs = file.read()
    kit = {}
    for category in specs.split('\n\n'):
        header, *lines = category.split('\n')
        cat, *_ = header.split(':')
        items = [Item(cat, line) for line in lines]
        kit[cat] = items
    return kit


def kit_cost(kit_list):
    return sum([item.cost for item in kit_list])


def main():
    kit_list = load_kit_list()
    player = Character(100, 0, 0)
    with open('input.txt') as file:
        boss_spec = file.read()
    match = BOSS_PATTERN.match(boss_spec)
    boss = Character(*(int(v) for v in match.groups()))
    winning_cost = find_min_gold_to_win(kit_list, player, boss)

    print(f'{winning_cost=}')


def find_min_gold_to_win(kit_list, player, boss):
    # 1 weapon, 0-1 armour, 0-2 rings
    kit_options = []
    for weapon in kit_list['Weapons']:
        for armour in kit_list['Armor'] + [None]:
            for ring1 in kit_list['Rings'] + [None]:
                for ring2 in kit_list['Rings'] + [None]:
                    option = [weapon, armour, ring1, ring2]
                    option = [o for o in option if o is not None]
                    kit_options.append(option)
    kit_options.sort(key=kit_cost)
    for kit in kit_options:
        player.reset()
        boss.reset()
        player.kit = kit
        winner = Character.fight(player, boss)
        if winner == player:
            break
    winning_kit = player.kit
    return kit_cost(winning_kit)


if __name__ == '__main__':
    main()
