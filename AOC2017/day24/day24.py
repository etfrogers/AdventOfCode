from typing import List


class Component:
    def __init__(self, str):
        tokens = str.split('/')
        self.A = int(tokens[0])
        self.B = int(tokens[1])

    def __str__(self):
        return '/'.join([str(self.A), str(self.B)])

    def get_other_for_attach(self, attach):
        other = None
        if self.A == attach:
            other = self.B
        elif self.B == attach:
            other = self.A
        return other

    @property
    def strength(self):
        return self.A + self.B


class Bridge:
    def __init__(self, lst=None):
        if lst is None:
            lst = []
        self.list = lst

    def get_frozen(self):
        return Bridge(tuple(self.list))

    def append(self, comp: Component):
        self.list.append(comp)

    def copy(self):
        new = Bridge(self.list.copy())
        return new

    def __str__(self):
        return ', '.join([str(b) for b in self.list])

    @property
    def strength(self):
        return sum([c.strength for c in self.list])

    @property
    def length(self):
        return len(self.list)


def add_component(attachement: int, current: Bridge, remainder: List[Component], bridge_list: List[Bridge]):
    if current.list:  # exclude empty bridges
        bridge_list.append(current.get_frozen())
    others = [c.get_other_for_attach(attachement) for c in remainder]
    possibles = [(c, other) for c, other in zip(remainder, others) if other is not None]
    if not possibles:
        return current
    else:
        for (comp, other) in possibles:
            new_remainder = [c for c in remainder if c is not comp]
            new_current = current.copy()
            new_current.append(comp)
            new_attachment = other
            add_component(new_attachment, new_current, new_remainder, bridge_list)


def make_bridges(components):
    attachment = 0
    bridges = []
    add_component(attachment, current=Bridge(), remainder=components, bridge_list=bridges)
    strengths = [b.strength for b in bridges]
    return bridges, strengths


def bridge_list_to_string(lst):
    return '\n'.join([str(b) for b in lst])


def max_strength_long_bridge(bridges):
    lengths = [b.length for b in bridges]
    max_len = max(lengths)
    longest_bridges = [b for b in bridges if b.length == max_len]
    strength = max([b.strength for b in longest_bridges])
    return strength


def main():
    with open('input.txt', 'r') as file:
        components = file.readlines()
    components = [Component(line) for line in components]
    print([str(c) for c in components])
    bridges, strengths = make_bridges(components)
    strength = max_strength_long_bridge(bridges)
    print(strength)


if __name__ == '__main__':
    main()
