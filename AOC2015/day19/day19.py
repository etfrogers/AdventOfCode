import re
from utils import KeyDefaultDict


def parse_input(specs):
    replacement_spec, molecule_spec = specs.split('\n\n')
    molecule = molecule_spec.strip()
    replacements = [tuple(line.split(' => ')) for line in replacement_spec.split('\n')]
    return replacements, molecule


REGEXES = KeyDefaultDict(re.compile)


def do_replacements(molecule, replacements):
    molecules = set()
    for from_, to in replacements:
        pattern = REGEXES[from_]
        for match in pattern.finditer(molecule):
            new_molecule = molecule[:match.start()] + to + molecule[match.end():]
            molecules.add(new_molecule)
    return molecules


def build_molecule(replacements, target, reverse=False, greedy=False):
    start = 'e'
    if reverse:
        start, target = target, start
        replacements = [(to, from_) for from_, to in replacements]
        molecule_filter = lambda x: len(x) > 0 and ('e' not in x or x == 'e')
    else:
        molecule_filter = lambda x: len(x) <= len(target)

    n_steps = 0
    if greedy:
        if not reverse:
            raise ValueError('Greedy cannot be true if reverse is false')
        replacements.sort(key=lambda x: len(x[0]), reverse=True)
        old_molecule = ''
        molecule = start
        while target != molecule and molecule != old_molecule:
            old_molecule = molecule
            n_steps += 1
            for from_, to in replacements:
                if from_ in molecule:
                    start = molecule.index(from_)
                    end = start + len(from_)
                    molecule = molecule[:start] + to + molecule[end:]
                    break
        if target != molecule:
            raise ValueError('Not found target')
    else:
        molecules = {start}
        latest_molecules = molecules.copy()
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

    n_steps = build_molecule(replacements, target=molecule, reverse=True, greedy=True)
    print(f'Part 2: Number of steps is {n_steps}')


if __name__ == '__main__':
    main()
