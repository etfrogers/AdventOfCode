import re
from collections import defaultdict


def parse_input(specs):
    replacement_spec, molecule_spec = specs.split('\n\n')
    molecule = molecule_spec.strip()
    replacements = [tuple(line.split(' => ')) for line in replacement_spec.split('\n')]
    return replacements, molecule


class RegexDict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


REGEXES = RegexDict(re.compile)


def do_replacements(molecule, replacements):
    molecules = set()
    for from_, to in replacements:
        pattern = REGEXES[from_]
        for match in pattern.finditer(molecule):
            new_molecule = molecule[:match.start()] + to + molecule[match.end():]
            molecules.add(new_molecule)
    return molecules


def build_molecule(replacements, target, reverse=False):
    start = 'e'
    if reverse:
        start, target = target, start
        replacements = [(to, from_) for from_, to in replacements]
        molecule_filter = lambda x: len(x) > 0 and ('e' not in x or x == 'e')
    else:
        molecule_filter = lambda x: len(x) <= len(target)
    molecules = {start}
    latest_molecules = molecules.copy()
    n_steps = 0
    while target not in molecules:
        n_steps += 1
        new_molecules = set()
        for molecule in latest_molecules:
            new_molecules.update(do_replacements(molecule, replacements))
        new_molecules = {mol for mol in new_molecules if molecule_filter(mol)}
        molecules.update(new_molecules)
        latest_molecules = new_molecules
        print(f'{n_steps}: {len(molecules)}')
    return n_steps


def main():
    with open('input.txt') as f:
        specs = f.read()
    replacements, molecule = parse_input(specs)
    generated_molecules = do_replacements(molecule, replacements)
    print(f'Part 1: Number of distinct molecules is {len(generated_molecules)}')

    n_steps = build_molecule(replacements, target=molecule)
    print(f'Part 2: Number of steps is {n_steps}')


if __name__ == '__main__':
    main()
