import re


def parse_input(specs):
    replacement_spec, molecule_spec = specs.split('\n\n')
    molecule = molecule_spec.strip()
    replacements = [tuple(line.split(' => ')) for line in replacement_spec.split('\n')]
    return replacements, molecule


def do_replacements(molecule, replacements):
    molecules = set()
    for replacement in replacements:
        pattern = re.compile(replacement[0])
        for match in pattern.finditer(molecule):
            new_molecule = molecule[:match.start()] + replacement[1] + molecule[match.end():]
            molecules.add(new_molecule)
    return molecules


def main():
    with open('input.txt') as f:
        specs = f.read()
    replacements, molecule = parse_input(specs)
    generated_molecules = do_replacements(molecule, replacements)
    print(f'Part 1: Number of distinct molecules is {len(generated_molecules)}')


if __name__ == '__main__':
    main()
