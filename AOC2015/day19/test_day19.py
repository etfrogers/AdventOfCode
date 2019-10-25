from AOC2015.day19.day19 import parse_input, do_replacements

test_input_1 = '''H => HO
H => OH
O => HH

HOH'''


test_input_2 = '''H => HO
H => OH
O => HH

HOHOHO'''


def test_parse_1():
    replacements, molecule = parse_input(test_input_1)
    assert len(replacements) == 3
    assert replacements[0] == ('H', 'HO')
    assert replacements[1] == ('H', 'OH')
    assert replacements[2] == ('O', 'HH')
    assert molecule == 'HOH'


def test_parse_2():
    replacements, molecule = parse_input(test_input_2)
    assert len(replacements) == 3
    assert replacements[0] == ('H', 'HO')
    assert replacements[1] == ('H', 'OH')
    assert replacements[2] == ('O', 'HH')
    assert molecule == 'HOHOHO'


def test_replacements_1():
    replacements, molecule = parse_input(test_input_1)
    generated_molecules = do_replacements(molecule, replacements)
    assert len(generated_molecules) == 4
    assert 'HOOH' in generated_molecules
    assert 'HOHO' in generated_molecules
    assert 'OHOH' in generated_molecules
    assert 'HHHH' in generated_molecules


def test_replacements_2():
    replacements, molecule = parse_input(test_input_2)
    generated_molecules = do_replacements(molecule, replacements)
    assert len(generated_molecules) == 7


def test_part_1():
    with open('input.txt') as f:
        specs = f.read()
    replacements, molecule = parse_input(specs)
    generated_molecules = do_replacements(molecule, replacements)
    assert len(generated_molecules) == 535
